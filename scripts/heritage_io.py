"""Bounded read-only heritage discovery; no extraction or evidence mutation."""

from __future__ import annotations
import fnmatch
import hashlib
import os
import stat
import struct
import tarfile
import zipfile
from pathlib import Path, PurePosixPath


def safe_relative(name):
    p = PurePosixPath(name)
    return (
        bool(name)
        and not p.is_absolute()
        and ".." not in p.parts
        and "\\" not in name
        and ":" not in name
        and "\x00" not in name
    )


def no_symlinks(path):
    return not any(p.is_symlink() for p in (path, *path.parents))


def open_regular(path):
    """Resolve every path component without following a symlink, including races."""
    path = path.absolute()
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[1:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=directory,
            )
            os.close(directory)
            directory = next_fd
        fd = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory
        )
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            raise ValueError("nonregular")
        return fd
    finally:
        os.close(directory)


def streamed_hash(path, limit):
    if not no_symlinks(path):
        raise ValueError("unsafe path")
    fd = open_regular(path)
    with os.fdopen(fd, "rb") as f:
        before = os.fstat(f.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("nonregular")
        if before.st_size > limit:
            raise OverflowError("oversize")
        h = hashlib.sha256()
        total = 0
        while block := f.read(1024 * 1024):
            total += len(block)
            if total > limit:
                raise OverflowError("oversize")
            h.update(block)
        after = os.fstat(f.fileno())
        current = path.lstat()

        def keys(s):
            return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

        if keys(before) != keys(after) or keys(after) != keys(current):
            raise ValueError("changed during read")
    return "sha256:" + h.hexdigest(), total


class MetadataReader:
    """Bound parser reads even if a concurrently altered header claims huge metadata."""

    def __init__(self, stream, budget):
        self.stream = stream
        self.budget = budget

    def read(self, n=-1):
        if n < 0:
            n = os.fstat(self.stream.fileno()).st_size - self.stream.tell()
        if n > self.budget:
            raise ValueError("archive metadata budget")
        block = self.stream.read(n)
        self.budget -= len(block)
        return block

    def seek(self, *a):
        return self.stream.seek(*a)

    def tell(self):
        return self.stream.tell()

    def seekable(self):
        return True


def archive_status(path, config):
    """Read bounded metadata only. Compressed TAR and ZIP64 remain unexamined."""
    maximum = config["max_archive_members"]
    size = config["max_archive_uncompressed_bytes"]
    try:
        with os.fdopen(open_regular(path), "rb") as source:
            magic = source.read(4)
            source.seek(0)
            if magic.startswith(b"PK"):
                source.seek(0, 2)
                length = source.tell()
                source.seek(max(0, length - 65557))
                tail = source.read(65557)
                offset = tail.rfind(b"PK\x05\x06")
                if offset < 0 or len(tail) - offset < 22:
                    return "UNREADABLE"
                (
                    _,
                    disk,
                    central_disk,
                    disk_entries,
                    entries,
                    metadata_bytes,
                    central_offset,
                    comment,
                ) = struct.unpack("<4s4H2LH", tail[offset : offset + 22])
                if disk or central_disk or disk_entries != entries:
                    return "UNSAFE"
                if (
                    entries == 65535
                    or metadata_bytes == 0xFFFFFFFF
                    or central_offset == 0xFFFFFFFF
                ):
                    return "OVERSIZE"
                if entries > maximum or metadata_bytes > 8 * 1024 * 1024:
                    return "OVERSIZE"
                if (
                    offset + 22 + comment != len(tail)
                    or central_offset + metadata_bytes > length
                ):
                    return "UNSAFE"
                source.seek(0)
                with zipfile.ZipFile(
                    MetadataReader(source, 8 * 1024 * 1024 + 131072)
                ) as z:
                    members = z.infolist()
                    if (
                        len(members) > maximum
                        or sum(m.file_size for m in members) > size
                    ):
                        return "OVERSIZE"
                    names = set()
                    for m in members:
                        if (
                            not safe_relative(m.filename)
                            or m.filename in names
                            or stat.S_ISLNK(m.external_attr >> 16)
                        ):
                            return "UNSAFE"
                        names.add(m.filename)
                return "SAFE_METADATA"
            if path.name.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
                return "UNREADABLE"
            if path.name.endswith(".tar"):
                if os.fstat(source.fileno()).st_size > 8 * 1024 * 1024:
                    return "OVERSIZE"
                total = 0
                names = set()
                with tarfile.open(
                    fileobj=MetadataReader(source, 8 * 1024 * 1024 + 65536), mode="r|"
                ) as t:
                    for index, m in enumerate(t):
                        total += m.size
                        if index >= maximum or total > size:
                            return "OVERSIZE"
                        if (
                            not safe_relative(m.name)
                            or m.name in names
                            or not (m.isfile() or m.isdir())
                        ):
                            return "UNSAFE"
                        names.add(m.name)
                return "SAFE_METADATA"
            return "NOT_ARCHIVE"
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile):
        return "UNREADABLE"


def discovered(root, patterns, errors=None):
    """Sorted metadata walk; excluded directories are pruned before descent."""

    def excluded(name):
        parts = PurePosixPath(name).parts
        return any(
            fnmatch.fnmatch("/".join(parts[:i]), p)
            for i in range(1, len(parts) + 1)
            for p in patterns
        )

    def failed(error):
        if errors is None:
            raise error
        errors.append(error)

    for current, dirs, files in os.walk(root, followlinks=False, onerror=failed):
        dirs.sort()
        files.sort()
        kept = []
        for name in dirs:
            p = Path(current) / name
            relative = p.relative_to(root).as_posix()
            if excluded(relative):
                continue
            if p.is_symlink():
                yield relative
            else:
                kept.append(name)
        dirs[:] = kept
        for name in files:
            relative = (Path(current) / name).relative_to(root).as_posix()
            if not excluded(relative):
                yield relative

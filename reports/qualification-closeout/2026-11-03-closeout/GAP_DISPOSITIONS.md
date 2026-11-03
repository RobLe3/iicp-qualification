# Bounded gap dispositions

The [register](gap-dispositions.json) assigns an owner, retained source digest,
status and next action to every category in this checkpoint’s **572 unique
object/gap pairs**. This is aggregate coverage of the reviewed private inventory,
not publication of private object locators or a claim that the gaps are resolved.

| Category | Count | Disposition |
|---|---:|---|
| Oversized | 556 | Unresolved; content exceeds the approved read bound. Prioritize a named claim before proposing bounded retrieval. |
| Unsafe | 1 | Unresolved; review metadata and ownership without following or bypassing the protected path. |
| Expected-hash mismatch | 15 | Preserve original classification. Dated source-delta evidence provides bounded original-byte retention, not approval or replacement of pins. |
| **Object/gap denominator** | **572** | **All categories have recorded dispositions; no gap is declared resolved.** |

The **1,250 frontier entries** are separate unexamined discovery work, not 1,250
additional object gaps. Excluded-path census and total historical execution count
remain unknown. Their owner and next action are recorded separately, without
inventing an aggregate historical denominator.

[Root issue #1676](https://github.com/RobLe3/iicp.network/issues/1676) remains the
coordination owner and stays open. This register does not authorize additional
reads beyond existing bounds, source repair, deletion, AWS activity or workloads.
Historical completeness remains false; qualification credit added remains zero.

"""Validate/render finite Directory witnesses; no product execution or acceptance."""
from pathlib import Path
import argparse
import hashlib
import json
from jsonschema import Draft202012Validator
from sdk_caller_reference import privacy

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'reports/postcert/2026-11-07-directory-kernels'
REVIEWED = {'attempt_history': [{'attempt_id': 'php-metadata-refusal',
                      'method_executions': 0,
                      'methods_failed': 0,
                      'methods_passed': 0,
                      'outcome': 'ADMISSION_REFUSED',
                      'predecessor': None,
                      'profile_id': 'php-sqlite'},
                     {'attempt_id': 'php-oci-failure',
                      'method_executions': 0,
                      'methods_failed': 0,
                      'methods_passed': 0,
                      'outcome': 'SETUP_FAILED',
                      'predecessor': 'php-metadata-refusal',
                      'profile_id': 'php-sqlite'},
                     {'attempt_id': 'php-layout',
                      'method_executions': 4,
                      'methods_failed': 1,
                      'methods_passed': 3,
                      'outcome': 'PARTIAL_ORACLE_FAILURE',
                      'predecessor': 'php-oci-failure',
                      'profile_id': 'php-sqlite'},
                     {'attempt_id': 'php-empty-oracle-successor',
                      'method_executions': 1,
                      'methods_failed': 0,
                      'methods_passed': 1,
                      'outcome': 'PASS',
                      'predecessor': 'php-layout',
                      'profile_id': 'php-sqlite'},
                     {'attempt_id': 'rust-selector-refusal',
                      'method_executions': 0,
                      'methods_failed': 0,
                      'methods_passed': 0,
                      'outcome': 'SELECTOR_REFUSED',
                      'predecessor': None,
                      'profile_id': 'rust-memory'},
                     {'attempt_id': 'rust-selector-successor',
                      'method_executions': 3,
                      'methods_failed': 0,
                      'methods_passed': 3,
                      'outcome': 'PASS',
                      'predecessor': 'rust-selector-refusal',
                      'profile_id': 'rust-memory'},
                     {'attempt_id': 'rust-native-topology',
                      'method_executions': 0,
                      'methods_failed': 0,
                      'methods_passed': 0,
                      'outcome': 'ADMISSION_REFUSED',
                      'predecessor': None,
                      'profile_id': 'rust-mysql'},
                     {'attempt_id': 'rust-linux-wrapper',
                      'method_executions': 0,
                      'methods_failed': 0,
                      'methods_passed': 0,
                      'outcome': 'POSTCOMPILE_WRAPPER_FAILED',
                      'predecessor': 'rust-native-topology',
                      'profile_id': 'rust-mysql'},
                     {'attempt_id': 'rust-retained-elf-successor',
                      'method_executions': 1,
                      'methods_failed': 0,
                      'methods_passed': 1,
                      'outcome': 'PASS',
                      'predecessor': 'rust-linux-wrapper',
                      'profile_id': 'rust-mysql'}],
 'evidence': [{'evidence_id': 'php-witness',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': 'cf0f7f348ae83995954bc3932bcecc3e7ced62840c33f2467c798c65a4939fea'},
              {'evidence_id': 'php-review',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '5086fab4e55fd0c6276d9041a0225db5ac8ec8d261a7c326884142298852c472'},
              {'evidence_id': 'php-oracle-reconciliation',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': 'd38a0bbdb7aa117eaefe25fb941503b705da22b568d365b8a85177867dd4fb21'},
              {'evidence_id': 'php-absence',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '775b9ccda6092f953d1bc05a099e685165b70520e708cb604914eb9be88404a5'},
              {'evidence_id': 'rust-memory-witness',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '3a17f805a4556f1935a43d402cec1ce6d28465e2a1d6186605fdbaeee78e7a6b'},
              {'evidence_id': 'rust-memory-review',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '73ddfed797a8ac5127e22f906b1971ed7a6761ecea5f7d951056847ec5fbde5e'},
              {'evidence_id': 'rust-mysql-witness',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '389f965f85f74bb89c564c52d1e2768d931941e788136fbc99717b88cd47d7c5'},
              {'evidence_id': 'rust-mysql-review',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '9c9a26c27c525e41122059f425c17c7b78bc45c961b10a18630fc51f450e8064'},
              {'evidence_id': 'rust-mysql-absence',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '8ea62b7e5d83fab37c8e24cd2cac20d1e9bb5db516adc31f81bd1bb33cb68195'},
              {'evidence_id': 'rust-mysql-producer',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': 'c9cb63837ec873d0203be274ba408ba6476a5bcac1b2fee2d7f57c9141f045a5'},
              {'evidence_id': 'rust-native-refusal',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '6847d983a44c1adf50ff9f85621a64e416acc6c2077b6a36a9b785d7b609a227'},
              {'evidence_id': 'rust-linux-wrapper-failure',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '27f9d95a1fc37f1f02cf459337221dd1ee1609dd7a7446a001ddbca8c65f8795'},
              {'evidence_id': 'php-private-test-source',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '952e6c56f3b003ebbb4813d33051e42f40206f06b3fa95caaf20d1dcaf7e7566'},
              {'evidence_id': 'rust-mysql-private-test-source',
               'original_bytes_public': False,
               'retention': 'PRIVATE_RETAINED_REVIEWED',
               'sha256': '248f1fc38a7901258760afa319706b10c49ddc5712bde0e38edba4c18b3261a6'}],
 'execution_profiles': [{'backend': 'SQLite memory / in-process Laravel HTTP kernel',
                         'component': 'php-directory',
                         'failed_method_executions': 1,
                         'method_executions': 5,
                         'passing_distinct_methods': 4,
                         'profile_id': 'php-sqlite',
                         'runtime': 'PHP 8.3.35 / Linux ARM64 container',
                         'source_commit': '2dfd228b49c587150a44f448cea1351a9f039d32',
                         'source_mode': 'Three original frozen methods plus one private test-only '
                                        'oracle'},
                        {'backend': 'InMemoryRepo / in-process HTTP kernel',
                         'component': 'rust-directory',
                         'failed_method_executions': 0,
                         'method_executions': 3,
                         'passing_distinct_methods': 3,
                         'profile_id': 'rust-memory',
                         'runtime': 'Rust/Cargo 1.98.0 / native macOS ARM64',
                         'source_commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                         'source_mode': 'Three original frozen methods; explicit source liveness '
                                        'bypass'},
                        {'backend': 'MySqlRepo / disposable tmpfs database / in-process HTTP '
                                    'kernel',
                         'component': 'rust-directory',
                         'failed_method_executions': 0,
                         'method_executions': 1,
                         'passing_distinct_methods': 1,
                         'profile_id': 'rust-mysql',
                         'runtime': 'Rust/Cargo 1.98.0 / Linux ARM64 container; MySQL 8.0.46',
                         'source_commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                         'source_mode': 'One new private cfg(test) method; explicit liveness '
                                        'bypass'}],
 'limits': ['These are selected post-certification observations, not the original qualification '
            'execution or an accepted successor.',
            'Different backends, runtime contexts and assertion depths are not a matched '
            'cross-platform or whole-implementation equivalence experiment.',
            'PHP uses SQLite memory, testing allowances and fake external health; one variant and '
            'selected fields do not prove arbitrary extension or complete node-list preservation.',
            'Rust memory tests use InMemoryRepo and explicit liveness bypass; passing methods do '
            'not establish MySQL behavior.',
            'The separate Rust MySQL method demonstrates fresh-connection readback on tmpfs, not '
            'process crash, restart or disk durability.',
            'All three profiles use an in-process HTTP kernel; real HTTP/TLS, production startup '
            'and security are not established.',
            'PHP original three passing methods were not repeated; its newly authored oracle '
            'failed once and only that corrected method was rerun. This is not a clean four-method '
            'single run.',
            'Native MySQL topology refusal and Linux postcompile wrapper failure remain failures. '
            'Successful retained-artifact execution does not establish the sole earlier glob '
            'cause.',
            'Raw responses and private execution records are not distributed. Digests identify '
            'retained sources but do not make them publicly reproducible.',
            'Whole capability contracts, complete supported-scope defect clearance, historical '
            'preservation, semantic IFRB, successor freeze, external interoperability and release '
            'readiness remain incomplete.'],
 'methods': [{'assertions': ['shared fixture exact pin'],
              'evidence_id': 'php-witness',
              'method': 'Tests\\Feature\\EffectiveCapabilityProfileTest::test_shared_fixture_is_exactly_pinned',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'php-sqlite'},
             {'assertions': ['one effective variant survives registration and node projection'],
              'evidence_id': 'php-witness',
              'method': 'Tests\\Feature\\EffectiveCapabilityProfileTest::test_effective_variant_survives_registration_and_node_projection',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'php-sqlite'},
             {'assertions': ['exact duplicate and duplicate variant identifiers refused'],
              'evidence_id': 'php-witness',
              'method': 'Tests\\Feature\\EffectiveCapabilityProfileTest::test_exact_duplicates_and_duplicate_variant_ids_are_rejected',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'php-sqlite'},
             {'assertions': ['empty capabilities refused with validation_error and unchanged node '
                             'count'],
              'evidence_id': 'php-witness',
              'method': 'Tests\\Feature\\PostcertEmptyCapabilityTest::test_empty_capabilities_refused_without_new_node',
              'origin': 'PRIVATE_TEST_ONLY',
              'outcome': 'PASS',
              'profile_id': 'php-sqlite'},
             {'assertions': ['HTTP kernel201 registration',
                             'same in-memory state discover',
                             'two variants retained',
                             'selected version,phase,variant,feature and optional-extension '
                             'assertions'],
              'evidence_id': 'rust-memory-witness',
              'method': 'tests::effective_capability_variants_survive_registration_and_discovery',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'rust-memory'},
             {'assertions': ['duplicate intent/variant and negative token limit refused'],
              'evidence_id': 'rust-memory-witness',
              'method': 'tests::registration_rejects_duplicate_capability_variants_and_invalid_limits',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'rust-memory'},
             {'assertions': ['malformed, duplicate and oversized profile sets refused'],
              'evidence_id': 'rust-memory-witness',
              'method': 'tests::registration_rejects_malformed_or_oversized_capability_profiles',
              'origin': 'ORIGINAL_FROZEN',
              'outcome': 'PASS',
              'profile_id': 'rust-memory'},
             {'assertions': ['two registered variants retained through fresh-pool node-detail and '
                             'discovery',
                             'six invalid inputs refused with 422 / validation_error',
                             'checked positive capability fields and one node / two capability '
                             'rows unchanged after each refusal'],
              'evidence_id': 'rust-mysql-witness',
              'method': 'tests::postcert_registration_persists_variants_and_refuses_invalid_mysql',
              'origin': 'PRIVATE_TEST_ONLY',
              'outcome': 'PASS',
              'profile_id': 'rust-mysql'}],
 'source_metadata': [{'commit': '2dfd228b49c587150a44f448cea1351a9f039d32',
                      'path': 'tests/Feature/EffectiveCapabilityProfileTest.php',
                      'repository': 'RobLe3/iicp-directory-php',
                      'sha256': '25f2235fb239c1eeaa5e163f33b2e82f2c8b52dbe2664e5e99d06de924b063c0',
                      'url': 'https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/tests/Feature/EffectiveCapabilityProfileTest.php'},
                     {'commit': '2dfd228b49c587150a44f448cea1351a9f039d32',
                      'path': 'bootstrap/app.php',
                      'repository': 'RobLe3/iicp-directory-php',
                      'sha256': '7ca622651c079da6b1ad6842b5aa5b2d5ed3b69afa1059239d685dce3b4920fe',
                      'url': 'https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/bootstrap/app.php'},
                     {'commit': '2dfd228b49c587150a44f448cea1351a9f039d32',
                      'path': 'app/Http/Controllers/RegisterController.php',
                      'repository': 'RobLe3/iicp-directory-php',
                      'sha256': '2ded78ffec0820fac57483a6f281e57ad214fd52d85bffb0cc19597f3c04403c',
                      'url': 'https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/app/Http/Controllers/RegisterController.php'},
                     {'commit': '2dfd228b49c587150a44f448cea1351a9f039d32',
                      'path': 'composer.lock',
                      'repository': 'RobLe3/iicp-directory-php',
                      'sha256': 'f811bb53f3a4862d8a7b0cc8095a39ecfae655f5447fc8ef94a3b58c62a85ad9',
                      'url': 'https://github.com/RobLe3/iicp-directory-php/blob/2dfd228b49c587150a44f448cea1351a9f039d32/composer.lock'},
                     {'commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                      'path': 'src/main.rs',
                      'repository': 'RobLe3/iicp-directory-rust',
                      'sha256': '9de172ee8f008ae43977e91a23dc66cf9cf499c31a74251944331d848577d1a9',
                      'url': 'https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/main.rs'},
                     {'commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                      'path': 'src/main_tests.rs',
                      'repository': 'RobLe3/iicp-directory-rust',
                      'sha256': '80672e4fe2c45ddd325e41e02df09e28bb24f6e19444dd004b2d57eac9446251',
                      'url': 'https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/main_tests.rs'},
                     {'commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                      'path': 'src/repo.rs',
                      'repository': 'RobLe3/iicp-directory-rust',
                      'sha256': '00a44453ef632cda1e5af47867a8de7c20dad52b231543d4df9e54b8032d053f',
                      'url': 'https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/repo.rs'},
                     {'commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                      'path': 'src/registration_store.rs',
                      'repository': 'RobLe3/iicp-directory-rust',
                      'sha256': 'c1e65f7aeb857d637dbef4716a956e295611ee32e24b80491e5834aa4e7b2234',
                      'url': 'https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/src/registration_store.rs'},
                     {'commit': 'b95a362ad8f974334994ca73cd20210388a2362f',
                      'path': 'Cargo.lock',
                      'repository': 'RobLe3/iicp-directory-rust',
                      'sha256': '4a47d155ad1eeed4587ed1b205788b9855d3027c0cbdceb28a5b932d98b15910',
                      'url': 'https://github.com/RobLe3/iicp-directory-rust/blob/b95a362ad8f974334994ca73cd20210388a2362f/Cargo.lock'}]}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def load():
    return json.loads((DATA / 'observations.json').read_bytes())

def exact_counts(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ('qualification_credit', 'method_executions', 'methods_passed',
                       'methods_failed', 'passing_distinct_methods', 'failed_method_executions'):
                if type(item) is not int:
                    raise ValueError('EXACT_INTEGER_REQUIRED:' + key)
            exact_counts(item)
    elif isinstance(value, list):
        for item in value:
            exact_counts(item)

def validate(value):
    Draft202012Validator(json.loads((DATA / 'observations.schema.json').read_bytes())).validate(value)
    privacy(value)
    exact_counts(value)
    for key, expected in REVIEWED.items():
        if value[key] != expected:
            raise ValueError('REVIEWED_FACT_CHANGED:' + key)
    evidence = {row['evidence_id'] for row in value['evidence']}
    profiles = {row['profile_id']: row for row in value['execution_profiles']}
    if len(evidence) != len(value['evidence']) or len(profiles) != len(value['execution_profiles']):
        raise ValueError('DUPLICATE_IDENTITY')
    seen = set()
    for attempt in value['attempt_history']:
        if attempt['attempt_id'] in seen or (attempt['predecessor'] is not None and attempt['predecessor'] not in seen):
            raise ValueError('ATTEMPT_LINEAGE')
        if attempt['method_executions'] != attempt['methods_passed'] + attempt['methods_failed']:
            raise ValueError('ATTEMPT_ACCOUNTING')
        seen.add(attempt['attempt_id'])
    for profile, record in profiles.items():
        attempts = [r for r in value['attempt_history'] if r['profile_id'] == profile]
        methods = [r for r in value['methods'] if r['profile_id'] == profile]
        if len({r['method'] for r in methods}) != record['passing_distinct_methods']:
            raise ValueError('METHOD_ACCOUNTING')
        for field, source in [('method_executions', 'method_executions'),
                              ('failed_method_executions', 'methods_failed')]:
            if sum(r[source] for r in attempts) != record[field]:
                raise ValueError('PROFILE_ACCOUNTING')
    if any(row['evidence_id'] not in evidence for row in value['methods']):
        raise ValueError('UNRESOLVED_EVIDENCE')
    return True

def render(value):
    validate(value)
    lines = ['# Directory registration and capability witnesses', '',
        'These are selected ordinary post-certification observations, not qualification receipts '
        'or a complete functional reference. They add **zero qualification credit** and do not '
        'change the accepted candidate, original evidence or five project-operated certificates.', '',
        '## Executed methods and environments', '',
        '| Profile | Backend | Passing distinct methods | Actual method executions | Failed method executions |',
        '|---|---|---:|---:|---:|']
    for row in value['execution_profiles']:
        lines.append('| ' + ' | '.join(str(row[k]) for k in ('profile_id', 'backend',
            'passing_distinct_methods', 'method_executions', 'failed_method_executions')) + ' |')
    lines += ['', 'The profiles are not a matched platform comparison. Do not add refusal inputs, '
        'assertions, synthetic controls and executed methods into a coverage percentage.', '',
        '### PHP / SQLite', '',
        'Three frozen EffectiveCapabilityProfileTest methods passed with 16 assertions. A new '
        'empty-capability method first failed on a Laravel-default response-shape expectation, '
        'after its 422 assertion passed. The original failed response body was not retained; '
        'no runtime error-code or unchanged-row claim is inferred for that failed attempt. '
        'Source review supported the existing IICP error envelope, not the new oracle. Only '
        'the corrected private method was rerun: it passed seven assertions, including validation_error '
        'and unchanged node count. The three original successes were not repeated. Four distinct '
        'methods therefore have passing evidence across five executions, not one clean four-method run.', '',
        '### Rust / InMemoryRepo', '',
        'Three original frozen methods passed once each: registration/discovery of two variants; '
        'duplicate variants and invalid limits; malformed, duplicate and oversized profile sets. '
        'The original selector expected the wrong test namespace and refused before method execution. '
        'A reviewed selector successor reused the existing build and listing. This in-memory evidence '
        'does not establish database persistence.', '',
        '### Rust / MySQL', '',
        'One new private cfg(test) method passed once. Actual HTTP-kernel registration used MySqlRepo. '
        'Two variants survived closure of the writer pool and readback through a fresh reader pool, '
        'node-detail and discovery. Six invalid inputs returned 422 / validation_error: empty '
        'capabilities, duplicate variants, negative token limit, malformed profile, duplicate profile '
        'and oversized profile set. Checked positive capability fields and one node / two capability '
        'row counts remained unchanged after each refusal.', '',
        'The native predecessor refused its actual host-port boundary before application execution. '
        'The Linux successor compiled successfully but its executable-discovery wrapper then failed '
        'before listing or application execution. A separately reviewed continuation reused the exact '
        'Cargo-produced ELF without rebuild or permission change. Successful execution does not '
        'establish the sole earlier glob failure cause. Both failures remain failures.', '',
        'The database was disposable tmpfs MySQL 8.0.46. Fresh-pool readback is not crash/restart or '
        'disk durability. Resource captures preceded exact-owned removal; separate parent-performed '
        'readback was inspected by an independent reviewer. This is not external certification.', '',
        '## Method-to-observation index', '']
    for method in value['methods']:
        lines += ['- `' + method['profile_id'] + ' / ' + method['method'] + '` (' +
                  method['origin'] + '): ' + '; '.join(method['assertions']) +
                  '. Retained evidence ID: `' + method['evidence_id'] + '`.']
    lines += ['', '## Exact source and evidence identities', '',
        'The source metadata records frozen implementation revisions and public source links. '
        'Private witness and review digests identify retained originals; public validation does '
        'not retrieve or reproduce those originals. Newly authored test-only methods are not '
        'represented as original qualification methods. Historical pending-review fields in original '
        'witness records are preserved; separate review records bind the later accepted observations.', '']
    for source in value['source_metadata']:
        lines.append('- [' + source['repository'] + ' / ' + source['path'] + '](' + source['url'] +
                     '), SHA-256 `' + source['sha256'] + '`.')
    lines += ['', '## Limits', ''] + ['- ' + s for s in value['limits']]
    lines += ['', '## Offline verification', '', '```sh',
        'python3.13 -B scripts/directory_kernel_reference.py check',
        'python3.13 -B -m unittest discover -s tests -p "test_directory_kernel_reference.py" -v', '```', '',
        'These commands validate reviewed metadata, closed schema, method/attempt accounting, '
        'lineage, source/evidence identities, sanitization, generated text and the manifest. '
        'They execute no Directory, database or workload. `render` regenerates only the package '
        'README and manifest; it does not publish. Obtain the expected manifest digest from the '
        'reviewed PR rather than trusting an arbitrary copy.', '',
        '[Root #1678](https://github.com/RobLe3/iicp.network/issues/1678) owns the executable reference; '
        '[#1676](https://github.com/RobLe3/iicp.network/issues/1676) owns historical inventory. '
        'The [enclosing source mapping](../2026-11-07-enclosing-capability/README.md) and '
        '[SDK caller observations](../2026-11-07-sdk-callers/README.md) remain separate evidence layers. '
        'This supplement does not close whole capability contracts, authorize a successor or establish release readiness.', '']
    return '\n'.join(lines)

def manifest():
    return {'schema': 'iicp.directory-kernel-public-manifest.v1', 'qualification_credit': 0,
            'files': {name: sha((DATA / name).read_bytes())
                      for name in ('observations.json', 'observations.schema.json', 'README.md')}}

def check_package():
    value = load()
    validate(value)
    if (DATA / 'README.md').read_text() != render(value):
        raise ValueError('STALE_GENERATED_NARRATIVE')
    if json.loads((DATA / 'manifest.json').read_bytes()) != manifest():
        raise ValueError('MANIFEST_MISMATCH')
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'render'))
    args = parser.parse_args()
    if args.command == 'render':
        value = load()
        validate(value)
        (DATA / 'README.md').write_text(render(value))
        (DATA / 'manifest.json').write_text(json.dumps(manifest(), indent=2, sort_keys=True) + '\n')
    else:
        check_package()
    print('PASS: finite Directory metadata only; no product execution or qualification credit')

if __name__ == '__main__':
    main()

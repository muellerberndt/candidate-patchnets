#!/usr/bin/env python3
"""Strict replay of immutable v1 evidence; no rewriting of scientific receipts."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
SUITE = HERE.parents[1]
PINNED_NAMES = (
    'PROTOCOL.md', 'THEOREM.md', 'SKEPTICAL_CONTROLS.md', 'model.py',
    'probe.py', 'test_model.py', 'adapter_h0.py', 'adapter_h16.py', 'adapter_h4.py',
)
KERNEL_NAME = 'cadence-flagship/experiments/local-observer-repair/kernel.py'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'Non-finite JSON constant: {value}')


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def canonical(value):
    # Unlike Python equality, this distinguishes True from 1 and 1 from 1.0.
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def require_identical(actual, expected):
    if canonical(actual) != canonical(expected):
        raise ValueError('Typed scientific result or source identity differs')


def validate_envelope(data):
    if type(data) is not dict or set(data) != {'elapsed_seconds', 'result'}:
        raise ValueError('Unexpected receipt envelope')
    elapsed = data['elapsed_seconds']
    if (type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or elapsed < 0 or type(data['result']) is not dict):
        raise ValueError('Invalid receipt metadata')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned_sources():
    paths = {name: HERE / name for name in PINNED_NAMES}
    paths[KERNEL_NAME] = WORKSPACE / KERNEL_NAME
    return {name: digest(path) for name, path in paths.items()}


def supplemental_sources():
    # contract.py was not pinned in the v1 main receipt. This establishes its
    # identity for this replay only, not retrospective original-run custody.
    paths = (SUITE / 'contract.py', HERE / 'verify_round.py',
             HERE / 'test_verification.py')
    return {str(p.relative_to(WORKSPACE)): digest(p) for p in paths}


def replay():
    receipt_path = HERE / 'search_receipt.json'
    receipt_digest = digest(receipt_path)
    receipt = read_json(receipt_path)
    validate_envelope(receipt)
    before = pinned_sources()
    supplemental_before = supplemental_sources()
    require_identical(before, receipt['result']['sources'])
    spec = importlib.util.spec_from_file_location('codex_context_strict_replay', HERE / 'probe.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    observed = json.loads(canonical(module.run()))
    after = pinned_sources()
    require_identical(after, before)
    require_identical(supplemental_sources(), supplemental_before)
    require_identical(digest(receipt_path), receipt_digest)
    require_identical(observed, receipt['result'])
    checks = observed['checks']
    if not checks or any(type(v) is not bool or v is not True for v in checks.values()):
        raise ValueError('A required check failed or has the wrong type')
    return {
        'schema': 'codex-finite-context-strict-verification/1',
        'scientific_receipt_sha256': receipt_digest,
        'original_source_pins': before,
        'supplemental_replay_source_pins': supplemental_before,
        'checks': len(checks),
        'primary_event_solves': len(observed['primary_trials']),
        'typed_replay_equal': True,
        'sources_unchanged_during_replay': True,
        'original_run_full_source_custody_proven': False,
        'core_replacement_ready': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true',
                        help='replay and compare the existing strict-verification receipt')
    args = parser.parse_args()
    path = HERE / 'verification_receipt.json'
    if path.exists() and not args.verify:
        raise FileExistsError('Refusing to overwrite strict-verification receipt')
    start = time.monotonic()
    result = replay()
    if args.verify:
        existing = read_json(path)
        validate_envelope(existing)
        require_identical(result, existing['result'])
    else:
        with path.open('x') as output:
            json.dump({'elapsed_seconds': time.monotonic() - start, 'result': result},
                      output, indent=2, allow_nan=False)
            output.write('\n')
    print(json.dumps({key: result[key] for key in
                      ('checks', 'primary_event_solves', 'typed_replay_equal',
                       'sources_unchanged_during_replay', 'core_replacement_ready')}))


if __name__ == '__main__':
    main()

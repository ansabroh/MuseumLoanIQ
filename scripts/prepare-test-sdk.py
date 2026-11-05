"""Reuse the official linter's verified release archive for gltest's broken URL.

Does not modify the SDK, contract, assertions, or test results.
"""
import hashlib
from pathlib import Path
import shutil
import subprocess

VERSION = 'v0.3.0-rc7'
SHA256 = 'e218a1854214681560351051f76fe2b878545cf3409455ef372d57014a88ca67'
subprocess.run(['genvm-lint', 'check', 'contracts/museum_loan_iq.py'], check=True)
name = f'genvm-universal-{VERSION}.tar.xz'
source = Path.home() / '.cache' / 'genvm-linter' / name
if not source.is_file():
    raise SystemExit(f'Official linter did not provide expected {VERSION} archive')
if hashlib.file_digest(source.open('rb'), 'sha256').hexdigest() != SHA256:
    raise SystemExit('Official release archive checksum mismatch')
target = Path.home() / '.cache' / 'gltest-direct'
target.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target / name)
print(f'Prepared checksum-verified {VERSION} SDK for direct-mode tests')

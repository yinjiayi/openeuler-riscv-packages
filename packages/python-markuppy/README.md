# python-markuppy 1.18

Official upstream v1.18 is fixed to commit
`abeb20b9a6d0157ea561ab00b21b8e42dc62b086`; the unsigned annotated tag
is not a cryptographic authenticity claim. The 12562-byte archive has SHA-256
`9c7ba86d5d9fb7b2b4be71c55496a18742c300eeff08e3e07895e92db07fc98d`.

The PEP 621 metadata and runtime declare version 1.18. Upstream's stale
legacy setup.py and README version strings are not rewritten. The existing
setuptools backend builds offline with no dependency downloads or isolation.

The default suite means the unchanged `python tests/run_tests.py` command:
five inline-style/script tests and four add_raw tests. Both staged-wheel
`%check` and installed-RPM smoke replay that original runner and all nine
tests from fresh scratch, with no source-package copy present. An import
guard checks every runtime import against the expected site-packages path
and original SHA-256. Installed QA additionally checks RPM ownership,
version and `rpm -V`. Python 3.11 bounds retain the original makeSuite API;
other interpreter versions and native hardware are not claimed.

All 13 original Git files, their mode/checksum manifest and the fixed archive
remain under `/usr/share/python-markuppy`. LicenseRef-Public-Domain means
the runtime's explicit public-domain permission, not Unlicense or CC0.
The complete MIT LICENSE, original runtime header and author notices are
retained. No test, source, feature or upstream workflow is patched.
The separately authored installed QA checker is Apache-2.0; the complete
license is retained as QA-LICENSE, independently of the upstream licenses.
GitHub tar group-writability is normalized away before copying originals;
the archive retains the Git executable bits. Installed retained source files
are non-executable data (0644), including the original runner. The default
documented invocation already calls Python explicitly; this prevents BRP
shebang rewriting without changing source bytes or omitting any test.

Local validation covers repository tooling and inert source verification
only. Target build, original test execution, installation, physical RPM/SRPM
and public publication require their separate CI acceptance gates.

The first exact-head target run39084540224 passed all nine original tests,
but the downstream checker expected single-line verbose unittest results.
The unchanged upstream tests have docstrings, so unittest prints the result
on a second description line. The checker now handles both standard formats
and requires the exact nine original test identities, unique successful
results, one nine-test summary, one OK, and no failures or skips. Regression
checks parse the captured real output plus one-line fixtures and reject
missing, duplicate, unexpected, failed or skipped tests and malformed summaries.
No upstream source, default invocation, origin/ownership/hash checks or test
is removed; a replacement target run must still prove build and installed QA.

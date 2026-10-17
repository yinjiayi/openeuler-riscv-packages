# python-click-default-group

Current official1.2.4, fixed v1.2.4/commit429c066978162c2cfabb14ea287aa6131413c324,
all9 Git files checked against the complete fixed archive. Actual full LICENSE
and README are BSD-3-Clause, retaining2015–2023 Heungsub Lee notice and terms;
the Public Domain packaging classifier is stale and not used as authority.
Five frozen Aug8 distribution lineage observations are linked in package.yaml;
they are discovery history, not current distribution version claims.

The selected original shared current GitHub Actions command is bare pytest,
retaining setup.cfg test.py discovery and all7 original functions/assertions.
Target CPython3.11 uses distroClick8.1.7/pytest7.4.4 and flit_core3.8 satisfying
original >=3.2,<4. Click and pytest in pyproject have no version pins. This is
an explicitly new target environment, not reproduction of the GHA Click8.1.6
or older interpreter/Click matrix. Entire GHA/legacyTravis configurations stay
unchanged, but legacy lint/missing setup.py invocation, coverage/Coveralls and
CI orchestration are unclaimed. No pin relaxation/filter/new skip is applied.

Source check uses staged wheel module. Installed smoke repeats the same bare
pytest against the actual RPM-owned module, with checksum/version/import-origin
and distribution metadata checks. All9 originals and full archive are also
RPM-owned; scratch tests/config copy every original except runtime module,
preventing source shadowing. Fresh child fail-closed import guard enforces the
selected site, inherited interpreter/pytest injection settings removed. No
upstream/default/backend/RPM/QEMU executes locally. A PR submission alone is
not target CI success, installed validation, merge or public release.

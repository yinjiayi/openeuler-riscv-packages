# python-retry

Current eSAMTrade Retry2 0.9.5, Python distribution `retry2`, import package
`retry`. The distinct invl `retry` distribution is not coinstalled or substituted.
Current AUR `python-retry`0.9.5-1 lineage and official PyPI/unique fixed Git tag
bind this fork; no older release is selected to simplify tests.

All16 original Git files are SHA-256/Git-blob verified and retained, including
all original requirements, tox config, upload scripts, LICENSE and AUTHORS.
The upstream Apache2 notice is preserved; full official Apache2 text is an
independent checksum-pinned Source1 and `%license` alongside that notice.

The selected original shared tox test command is exact unfiltered `py.test`
on target Python3.11: all11 original test functions remain unchanged, without
new skip, xfail, expression filter or test replacement. All selected original
dependency lists remain supplied: decorator>=3.4.2,pbr,pytest,tox,wheel.
Legacy Python2.6/2.7/3.4/3.5/PyPy matrix, separate flake8 Python3.4 lint job and
external upload scripts are retained but unvalidated/unexecuted, not claimed
as passed checks. No original tests or runtime files are patched.

Offline PBR wheel generation uses PBR_VERSION=0.9.5, equal to original
setup.cfg and fixed release tag, because the fixed Git archive has no .git.
No dependencies are downloaded during builds and no pin is relaxed.

Source `%check` runs against the staged wheel, not the source module; installed
smoke repeats the same whole original command against RPM-owned installed
runtime with exact3 module hashes, metadata distribution/version, and origin
checks. All originals remain intact in the RPM. A temporary test cwd omits
only its source runtime copy to prevent shadowing; import guards fail closed
on any source fallback. This does not remove any original test or assertion.

Local validation is trusted repository policy/test/golden/source verification
only. No local upstream/default/backend/RPM/QEMU execution is performed;
target compilation, original tests and installed checks remain CI acceptance
gates. New PR submission does not mean build success, merge or publication.

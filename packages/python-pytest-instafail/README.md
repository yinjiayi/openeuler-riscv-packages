# python-pytest-instafail

Fixed upstream 0.5.0, tag v0.5.0, commit aab3a1e8f899584b9b31a56daf9f61cdc206a088.
Official archive SHA-256: f8de1f7e72ae7fd23d46dd60863ac4b26d6d3531715c44ca4c6ed40b98d7bf5a.
The complete BSD-3-Clause LICENSE and all 11 Git originals are preserved unchanged.

The build and installed smoke replay the original bare `pytest` command,
`setup.cfg` color setting and upstream CI `FORCE_COLOR=1`, without filters,
new skips, xfails or source changes. All seven original methods and both
three-way fixture parameter sets remain. The original Option constructor
sets n=None; worker-labelled fixture cases therefore do not establish real
xdist-worker execution. The legacy pytest5/6 tox interpreter/platform matrix
is preserved but unclaimed. Target Python3.11/distro pytest >=5 compatibility
is a separate CI gate, not a statement that the older tox environments ran.

The RPM retains the complete immutable archive and original-file manifest.
Both default-test routes copy unchanged non-runtime originals to isolated
temporary directories and run against wheel/RPM-owned runtime bytes and
metadata. A sitecustomize import-origin guard applies to pytest subprocesses
and PDB children. Installed payloads are checked with rpm -qf. No local
upstream/backend/default or RPM/QEMU build was performed during intake.

Runtime requires pytest >=5; original tests require pexpect and pytest-xdist.
No RISC-V patch is proposed. Full current dependency closure/EVR review,
fresh namespace/provider admission, trusted repository validation, actual
target CI and physical products remain separate acceptance gates.

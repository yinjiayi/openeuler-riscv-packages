# Math::SparseVector for openEuler RVA23

This package pins the official TPEDERSE CPAN Math-SparseVector 0.04 archive
to SHA-256 `8f6285132507fc88e9fe1c5c53c47dd25c94b1783cd4cc301833fc9e9e446823`,
matching publisher `T/TP/TPEDERSE/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-sparsevector-perl` 0.04-2build1 and Debian 0.04-2. The official
openEuler 24.03 LTS SP3 riscv64 RVA23 primary metadata has neither
`perl-Math-SparseVector` nor `perl(Math::SparseVector)` and supplies the
MakeMaker and Test::More providers for unchanged build and test.

The module, README, and installed `Math/INSTALL.pod` attribute Amruta
Purandare, Ted Pedersen, and Mahesh Joshi and expressly grant GNU GPL version
2 or later. The RPM uses `GPL-2.0-or-later` and installs README as its license
notice. No source or test is modified, and no bundled file has a contrary
notice.

`%check` runs the sole original default t/ file. Clean local execution passed
20 assertions with zero skips. Installed smoke verifies RPM/module ownership,
version, sparse norm and dot product, and deallocation. Target RPM/QEMU and
physical RPM/SRPM results require exact-head hosted PR CI; PR CI does not
establish public repository publication.

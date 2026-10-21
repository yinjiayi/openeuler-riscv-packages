# udns

This directory packages udns 0.6 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot records Arch stable Extra, Debian stable,
Fedora 44, openSUSE Tumbleweed, and Ubuntu 26.04 LTS. The distribution
metadata used two URL aliases; both resolve to the same official udns
component and are deduplicated here. No distribution packaging was executed.

The official project page names 0.6 as the current stable release and links
the versioned source archive. Independent retrieval produced the SHA-256 in
`sources.yaml`; the archive has one `udns-0.6/` root, no unsafe paths, and the
LGPL-2.1 license text. Source headers explicitly permit later LGPL versions.

Upstream supplies no standalone test target. The RPM therefore builds both
static and shared variants plus the official tools, then links and executes a
small version probe against the built shared library. Installed smoke checks
remain local and never issue DNS queries.

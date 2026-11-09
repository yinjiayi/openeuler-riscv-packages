<!-- SPDX-License-Identifier: Apache-2.0 -->
# Config::File 1.54

Noarch Perl configuration-file parser for openEuler 24.03 LTS SP3,
riscv64/RVA23. Frozen Ubuntu and Debian stable identify libconfig-file-perl
1.54-2. Only the fixed upstream CPAN release is used, not distro recipes.

The original module POD explicitly grants GPL v2 or later, names its
copyright holders, and ships complete GPLv2 text in LICENSE. The
MetaCPAN source SHA-256 and author's CPAN CHECKSUMS agree. The 2021
PAUSE index's historical SHA-1 signature and expired subkey are advisory
index evidence, not a detached archive signature; the full archive
SHA-256 is mandatory.

The original Build.PL uses the installed Module::Build and no vendored
helper. The unchanged default Build test runs functional fixtures, POD
syntax and POD coverage. Explicit POD dependencies and a load check keep
the original optional syntax test active. The installed smoke exercises
variable substitution, nested keys and an escaped comment marker.
No source patch is needed. Local host tests are separate from target CI.

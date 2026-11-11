<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodule-locate-perl

This directory packages [Module::Locate 1.80](https://metacpan.org/release/NEILB/Module-Locate-1.80) as `perl-module-locate` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed CPAN archive matches the PAUSE-signed directory checksum. The source and generated build metadata retain the upstream Perl license terms; the exact Dist::Zilla 5.037 generator license is included separately. The RPM runs the unchanged `make test TEST_VERBOSE=1` suite (five files, 50 assertions); the install smoke test exercises lookup and path conversion from the installed module.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

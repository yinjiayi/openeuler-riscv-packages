<!-- SPDX-License-Identifier: Apache-2.0 -->
# angie-mod-njs

This directory packages upstream `https://github.com/nginx/njs` version `1.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned release archive expands beneath `njs-1.0.0`; the RPM prep stage names
that source root explicitly. njs uses its own shell configure interface rather
than Autoconf; the build passes the RPM linker hardening flags through that
interface. The build also installs the PCRE2 development package required by
njs's configure-time regular-expression checks.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

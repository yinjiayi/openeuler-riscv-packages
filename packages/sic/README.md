<!-- SPDX-License-Identifier: Apache-2.0 -->
# sic

This directory packages upstream `https://tools.suckless.org/sic/` version `1.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official page-linked fixed release: https://dl.suckless.org/tools/sic-1.3.tar.gz
SHA-256: `30478fab3ebc75f2eb5d08cbb5b2fedcaf489116e75a2dd7197e3e9c733d65d2`.
All nine release files were reviewed. Frozen component `tools.suckless.org-sic`
retains AUR/Debian/Ubuntu lineage; no foreign recipe was executed.

The main license is MIT; strlcpy.c retains Todd Miller's ISC notice and arg.h
its original permissive copying notice. Both subpackages ship LICENSE,
complete strlcpy.c and arg.h as license material. No original file is patched
and no default feature is removed. Original make all remains intact. Upstream
has no test/check target. Five added functional groups cover version/error
behavior, login, server PING/messages/nickname, client commands and output/EOF.
The same checker runs on build, staged and installed binaries using only a
private 127.0.0.1 mock server, never the public IRC default. Upstream -v exits 1;
the check expects this original behavior. Tests fail on mismatches/timeouts.

gcc, glibc-devel, make, tar, gzip, coreutils, sed and Python 3 are required for
the locked target build/check. No external build network is used. QEMU
functional proof is not native timing, network-security or Internet IRC
interoperability proof. Initial PR creation is not successful target build
acceptance; full CI and physical RPM/SRPM qualification remain merge gates.

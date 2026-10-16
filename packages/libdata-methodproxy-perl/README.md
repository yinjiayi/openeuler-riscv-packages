<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::MethodProxy 0.05

The frozen Ubuntu `libdata-methodproxy-perl` key maps to the official
[Data-MethodProxy 0.05](https://metacpan.org/dist/Data-MethodProxy) CPAN
release. The publisher's author-directory `CHECKSUMS` and an independent HTTPS
download agree on SHA-256 `9cb6f97432b148e1d105eb3469e1f54acd38a672b129b68064a61e25fa6af9b2`.
The archive contains ordinary files in one top-level tree, without traversal
paths. Its `LICENSE` and `Data::MethodProxy` POD grant redistribution under
Perl's GPL/Artistic terms. The `Config::MethodProxy` compatibility module POD
points to the same grant; no bundled file presents a conflicting license.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-MethodProxy` RPM nor a `perl(Data::MethodProxy)` or
`perl(Config::MethodProxy)` provider. It uniquely supplies the declared hard
dependencies, including `perl-Module-Build-Tiny` 0.047, `perl(Module::Runtime)`
0.016, and `perl(Test2::V0)` 0.000155, satisfying upstream minima.
Both default upstream test files remain unchanged: local `./Build test` passes
10 assertions without skips after `./Build build`. Exact-head target CI must
prove the full test suite, target RPM build and installed functional smoke.
PR CI products do not establish public RPM publication.

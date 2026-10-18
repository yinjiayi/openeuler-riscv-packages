<!-- SPDX-License-Identifier: Apache-2.0 -->
# libprobe-perl-perl

This package maps the frozen inventory's exact libprobe-perl-perl key to
the official [Probe-Perl 0.03](https://metacpan.org/dist/Probe-Perl) CPAN
release. The official CPAN CHECKSUMS SHA-256 and an independent HTTPS
download agree on d9e4d21e2e77638559045fa09046b1b6fff6c403b949929db213e30abe8a3c31.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its included LICENSE grants the same GPL/Artistic
choice as Perl. CI verifies the pinned source before building for
openEuler 24.03 LTS SP3 riscv64/RVA23.

The official target Everything repository's SHA-256-verified primary metadata
contains no perl-Probe-Perl RPM or perl(Probe::Perl) provider; the required
core Perl/MakeMaker/Test modules are available. This is distinct from the
frozen inventory's external Ubuntu discovery row.

Upstream registers t/basic.t (19 assertions) and t/author-critic.t.
The RPM check runs the unmodified default make test: basic.t executes, while
the author-only critic file explicitly skips when AUTHOR_TESTING is unset.
Its optional Test::Perl::Critic author gate is not represented as passing.
The installed-RPM smoke checks the module version, Perl configuration,
interpreter discovery, and interpreter identity. This is a prerequisite for
the frozen-inventory libalgorithm-checkdigits-perl candidate; that package
remains deferred until the dependency is actually available to target CI.
CI build artifacts are not evidence of public RPM repository publication.

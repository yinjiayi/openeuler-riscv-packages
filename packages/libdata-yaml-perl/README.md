<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::YAML 0.0.7

The frozen Ubuntu `libdata-yaml-perl` 0.0.7-3 key maps to the official
[Data-YAML 0.0.7](https://metacpan.org/dist/Data-YAML) release. An independent
download of the 12,938-byte HTTPS archive and the publisher's author-directory
`CHECKSUMS` agree on SHA-256
`b82b53f5e5164cb7938cc3105a0ccaefb4fadcbf07d75ebb3578df9e2026deba`.
The archive has a single top-level tree, only regular files and directories,
and no traversal paths.

Copyright holder Andy Armstrong explicitly grants redistribution under Perl's
terms in the release README and each of the three installed PM files. The
Reader credits Adam Kennedy's YAML::Tiny template and regular expressions;
Kennedy's [official YAML::Tiny POD](https://metacpan.org/release/ADAMK/YAML-Tiny-1.51/view/lib/YAML/Tiny.pm)
independently grants those same terms. No archive file states conflicting
terms. The SPEC records the Perl GPL-or-Artistic choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Data-YAML` RPM or `perl(Data::YAML)`, Reader, or Writer provider. It
uniquely supplies MakeMaker 7.70, Test::More 1.302198, Test::Pod 1.52,
Test::Pod::Coverage 1.10, and the other hard build dependencies.

The seven unchanged default upstream `t/` files pass locally with 296
assertions, but `t/pod-coverage.t` skips locally because its module is absent.
The SPEC hard-requires the available target provider. Exact-head target CI
must prove all seven files run without skips, plus a built RPM/SRPM, DNF
installation, and installed reader/writer round-trip smoke. PR CI does not
establish public RPM publication.

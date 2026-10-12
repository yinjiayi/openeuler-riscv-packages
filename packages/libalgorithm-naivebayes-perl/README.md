<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-naivebayes-perl

This package maps the frozen inventory's exact `libalgorithm-naivebayes-perl`
key to the official [Algorithm-NaiveBayes 0.04](https://metacpan.org/dist/Algorithm-NaiveBayes)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `fd769448ec977a3626a135b02e0d5fcd41de2d9d14ade0632194d1ad801eeccd`.
The archive contains one top-level tree, only regular files and directories,
and no traversal paths. The module's `COPYRIGHT` POD grants redistribution
under the same terms as Perl itself; there is no separate LICENSE file in
this upstream release. CI verifies the pinned source before building for
openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Algorithm-NaiveBayes` RPM nor a `perl(Algorithm::NaiveBayes)`
provider. It does contain the required Perl core modules, MakeMaker, and
module-generator packages. This target check is distinct from the frozen
inventory's external Ubuntu discovery record.

Upstream registers three default tests: basic training and prediction,
discrete-model prediction, and a stored-model roundtrip. `%check` runs all
three unchanged (23 assertions). The RPM installation smoke checks the
installed version, trains and predicts with the frequency model, and loads
the discrete model. Local pure-Perl tests passed on macOS, but only exact-head
CI can establish the target RPM/QEMU result. PR CI artifacts do not establish
public RPM repository publication.

<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Validate::Type 1.6.0

The frozen Ubuntu `libdata-validate-type-perl` 1.6.0-2 key maps to the
official [Data-Validate-Type v1.6.0](https://metacpan.org/dist/Data-Validate-Type)
CPAN release. An independent download of the 19,866-byte HTTPS archive and
publisher `CHECKSUMS` agree on SHA-256
`5fb3c535906cff5064ce29307f96166ec02819818983dd72c6ea991943cd928d`.
The archive has a single top-level tree, only regular files and directories,
and no traversal paths.

Copyright holder Guillaume Aubert explicitly permits redistribution under
Perl 5 terms in the bundled `LICENSE`, sole installed module POD, and
`t/LocalTest.pm` POD. The license text spells out GPL version 1 or later or
Artistic 1.0. No ordinary archive file states conflicting terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Validate-Type` RPM nor a `perl(Data::Validate::Type)` provider.
It uniquely supplies Data::Dump 1.25, Scalar::Util 1.63, Test::Exception
0.43, Test::FailWarnings 0.008, Test::More 1.302198, and the remaining hard
build/runtime dependencies.

All thirteen original default `t/*.t` files remain in `%check` via the
upstream Module::Build route. `xt/` is an optional author suite enabled by
upstream only when `RELEASE_TESTING` is set; it is not the default suite.
The local Mac lacks Test::FailWarnings, so the full upstream suite cannot be
claimed as locally passed. Exact-head target CI must prove all thirteen run
without skips, along with a built RPM/SRPM, DNF installation, and installed
boolean-function smoke. PR CI does not establish public RPM publication.

<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::StreamSerializer 0.07

The frozen Debian `libdata-streamserializer-perl` 0.07-3 inventory key maps to
official stable [Data-StreamSerializer 0.07](https://metacpan.org/dist/Data-StreamSerializer).
Publisher CHECKSUMS and the independently downloaded 147,455-byte HTTPS archive
agree on SHA-256
`73334df3360c91dd480072fa5b4df790db83e79e31d9a6bdd5032d378b619668`.
The archive has one top-level tree and regular files/directories.

The frozen inventory recorded a license-review hold because release metadata
labels the license `unknown`. The archive itself includes `debian/copyright`
from upstream author and Debian maintainer Dmitry E. Oboukhov. It explicitly
grants `Files: *` redistribution under Artistic or GPL-1-or-later; the bundled
third-party `ppport.h` separately grants same-as-Perl terms. The installed
module POD repeats the same-as-Perl grant. The README retains an upstream
template sentence, but its following copyright-holder grant and the
file-scoped `debian/copyright` resolve that ambiguity for this fixed archive.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Data-StreamSerializer` package or `perl(Data::StreamSerializer)` provider.
It supplies GCC 14.3.1, Perl and perl-devel 5.38.0, ExtUtils::MakeMaker,
Test::More, and all core/default-test modules. No third-party runtime library
is needed.

All five unchanged default `t/*.t` files contain 70 assertions. The first
local macOS `make test` compiled XS but failed at hardened `dlopen` because
upstream tests prepend relative `blib/arch`. Re-running the same files from a
neutral directory with absolute `PERL5LIB` passed 70/70 with zero skips;
`B::CV` identified `_next` as an XSUB and a serialization probe produced
output. `%check` and installed smoke explicitly assert XS activation. Target
CI must prove the full riscv64 suite, physical RPM/SRPM products and DNF
installed smoke. PR CI is not repository publication.

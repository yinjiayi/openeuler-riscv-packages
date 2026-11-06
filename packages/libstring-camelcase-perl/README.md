<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-camelcase-perl

The frozen inventory's exact `libstring-camelcase-perl` key maps to Ubuntu
source version 0.04-2. This package uses the official stable
[String-CamelCase 0.04](https://metacpan.org/dist/String-CamelCase) CPAN
release. Its HTTPS tarball SHA-256
`89c3debceeceae8764f45d74023f8fbeee2d88399af67541dbdaa0b2bf2711a9`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. README, module POD and the bundled build helper all grant the same
terms as Perl itself despite frozen metadata reporting an unknown license;
README is installed as `%license` because no separate license text ships.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-CamelCase` nor a `perl(String::CamelCase)`
provider. It has Test::Pod 1.52 and Test::Pod::Coverage 1.10, both declared
as BuildRequires so the default upstream POD files must execute. This is a
snapshot check, not a guarantee about future repository contents.

The unmodified upstream local `make test` ran all six default `t/*.t` files
and reported 31 TAP items: the functional, load, boilerplate and POD checks
passed, while one conditional POD coverage file skipped because the local
machine lacks Test::Pod::Coverage. That skip is not counted as a pass; target
CI must verify the coverage test with the required dependency installed.
Upstream `Makefile.PL` warns that its MANIFEST lists a missing SIGNATURE;
there is no signature to verify, so the publisher CHECKSUMS SHA-256 is the
source-integrity evidence. A source-level staging install yielded the module
and manual page, both listed in the SPEC. Installed-RPM smoke tests version,
generated Provides and camelize/decamelize/word-split behavior. Target RPM
build, full default suite and installed smoke remain for CI to verify;
successful PR artifacts alone do not prove public repository publication.

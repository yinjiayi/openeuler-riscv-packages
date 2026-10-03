<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-classapi-perl

The frozen inventory's exact `libtest-classapi-perl` row maps to
[Debian source 1.07-2](https://packages.debian.org/source/sid/libtest-classapi-perl)
and [CPAN Test-ClassAPI 1.07](https://metacpan.org/dist/Test-ClassAPI).
The publisher's `E/ET/ETHER/CHECKSUMS` and the downloaded official HTTPS
archive both have SHA-256
`30e9dbfc5e0cc2ee14eae8f3465a908a710daecbd0a3ebdb2888fc4504fa18aa`.
The 34 archive entries form one safe top-level tree without path traversal,
links or special files. Its distribution-wide `LICENSE` explicitly permits
GNU GPL version 1 or later or Artistic License 1.0. The module has the same
copyright grant; there is no vendored code.

The official openEuler 24.03 LTS SP3 RVA23 `everything` `repomd.xml` pins
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That metadata has neither `perl-Test-ClassAPI` nor `perl(Test::ClassAPI)`.
It does provide all declared minimum runtime and test dependencies:
`perl(Class::Inspector)` 1.36, `perl(Config::Tiny)` 2.29,
`perl(Params::Util)` 1.07, `perl(File::Spec)` 3.88, and
`perl(Test::More)` 1.302198. This snapshot is not proof of later public
repository availability.

`%check` preserves all five original default upstream test files. A local
Perl 5.34.1 attempt failed because this Mac lacks `Config::Tiny` 2.00; it
is not target success evidence. Exact-head target CI must prove the full
original test suite and the installed-RPM smoke's two-assertion class API
fixture. A successful PR CI still does not prove public RPM publication.

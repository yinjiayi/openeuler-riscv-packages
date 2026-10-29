<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmime-base64-urlsafe-perl

This package maps Ubuntu's `libmime-base64-urlsafe-perl` source to the
official CPAN MIME::Base64::URLSafe 0.01 release. Its 2,404-byte archive has
SHA-256 `cb9966c50538bb676ab67bc40a7c841019b23ba2243d0ffcc2ccf084e5c33798`,
matching the publisher's `CHECKSUMS`. The archive has one root, no links or
traversal entries, and one default `t/*.t` file with 17 assertions.

The archived module and README explicitly grant redistribution and modification
on the same terms as Perl version 5.8.7 or later. Perl 5's documented dual
grant supports `GPL-1.0-or-later OR Artistic-1.0-Perl`; the archived README is
installed as the RPM license notice. The source metadata omits a machine-readable
license field, so the package uses the actual archived grant rather than
interpreting that omission as a restriction.

The official openEuler 24.03 LTS SP3 RVA23 primary metadata (compressed SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-MIME-Base64-URLSafe` nor
`perl(MIME::Base64::URLSafe)`. It supplies `perl(MIME::Base64)` 3.16 and the
Perl build/test providers. This is a snapshot, not a future availability
guarantee.

`%check` retains the complete upstream default `make test`. Installed-RPM
smoke checks the provider and URL-safe alphabet, decoding, padding and binary
round trips. No local RPM or QEMU build was run; target behavior requires
exact-head PR CI. CI artifacts are not repository publication.

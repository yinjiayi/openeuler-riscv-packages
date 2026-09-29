<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmailtools-perl

This package maps the frozen inventory's exact `libmailtools-perl` key to
the official [MailTools 2.22](https://metacpan.org/dist/MailTools) CPAN
release. Its HTTPS archive was independently downloaded and pinned to SHA-256
`3bf68bb212298fa699a52749dddff35583a74f36a92ca89c843b854f29d87c77`.
The archive contains one top-level tree, no traversal paths, links, or special
files. CI verifies the pinned digest before building for openEuler 24.03 LTS
SP3 `riscv64`/RVA23.

The standard upstream `t/` suite contains seven test files; `%check` runs all
of them and the extended `xt/99pod.t` POD test. The installed-RPM smoke verifies the version, Mail::Header behavior,
and Mail::Mailer construction without sending mail. The distribution declares
Date::Format, Date::Parse, Net::Domain, Net::NNTP, and Net::SMTP dependencies, retained
in the RPM metadata. It supplies `Mail::Mailer`, one prerequisite of
libytnef's optional `ytnefprocess` tool; it does not supply MIME::Parser.

MailTools uses the same GPL/Artistic choice as Perl itself. CI build artifacts
are not evidence of publication to the public RPM repository.

<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-spiffy

The frozen inventory's canonical `perl-spiffy` component merges Arch,
Fedora and openSUSE names with the Debian/Ubuntu `libspiffy-perl` alias.
It maps to the official stable [Spiffy 0.46](https://metacpan.org/dist/Spiffy)
CPAN release. The HTTPS tarball SHA-256
`8f58620a8420255c49b6c43c5ff5802bd25e4f09240c51e5bf2b022833d41da3`
matches the publisher's `CHECKSUMS` entry. The archive has one root, only
regular files and directories, and no traversal or special files. No AUR
recipe was executed or treated as source evidence.

The included LICENSE grants redistribution under the same terms as Perl 5
and includes the GPL version 1 and Artistic license texts. The README and
module POD repeat those terms. The RPM uses `GPL-1.0-or-later OR
Artistic-1.0-Perl` and installs LICENSE as `%license`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Spiffy` nor `perl(Spiffy)`. It does provide the runtime
capabilities `perl(Filter::Util::Call)`, `perl(Scalar::Util)`,
`perl(Data::Dumper)`, and `perl(YAML)` used in the module's conditional paths.
This is a snapshot check, not a guarantee about future repository contents.

All 31 functional default upstream `t/*.t` files passed 198 assertions
locally without modifying source. The remaining file is an upstream
release-candidate-only POD check and skips under normal conditions; the
SPEC retains it. A source-level staging install yielded Spiffy.pm,
Spiffy.pod, Spiffy/mixin.pm and the manual page, all listed in `%files`.
Installed-RPM smoke checks module/provider identity, a field round-trip,
and the mixin module. Target RPM build, tests, installed smoke and any public
publication remain for CI or later evidence to verify.

The dependent Test::Base package should not be submitted to target CI merely
because this PR exists: its Spiffy dependency needs an actual published
target repository provider first. String::Diff also remains held until its
Test::Base test dependency is available.

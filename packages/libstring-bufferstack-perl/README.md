<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-bufferstack-perl

The frozen inventory's exact key maps to the official
[String-BufferStack 1.16](https://metacpan.org/dist/String-BufferStack) CPAN
release. Its official HTTPS archive SHA-256 is
`812181c2e73ebb71b3c687bbb7aed97bb8b66df2a64d18bd8843dc0c4b083392`,
identical to the publisher's `CHECKSUMS` entry. All 27 archive entries are
under one top-level directory and are regular files or directories; no link,
special file, or traversal path is present. The bundled README and module POD
grant the same terms as Perl itself. This resolves the frozen catalog's
unknown-license marker; the RPM declares the Perl dual-license expression.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata has SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-String-BufferStack` nor a
`perl(String::BufferStack)` provider. It includes the declared Perl build and
test toolchain. This is a snapshot collision check, not a future guarantee.

`%check` runs all five default upstream tests (169 assertions passed on
local Perl 5.34.1). Initial target run `36796657542` failed in `%build`
before tests because Perl 5.38 did not search the source tree for the
bundled `inc::Module::Install`. The SPEC now explicitly adds that verified
source tree to `PERL5LIB` for configuration. This uses the release's bundled
build helper rather than substituting the independently versioned target
`perl-Module-Install` package, and does not drop or change tests. The
generated Makefile's test harness searches `inc`, `blib/lib`, and `blib/arch`.
The installed-RPM smoke checks module version, nesting, flushing, and
automatic provider metadata. The repaired exact-head target CI must still
establish the SP3 RVA23 RPM build, full suite, and installed smoke.

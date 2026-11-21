<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-ipc-run-safehandles

IPC::Run::SafeHandles 0.04 provides safe standard handles around Perl IPC::Run
and IPC::Run3 calls. This is a pure-Perl, vendorlib/noarch package for openEuler
24.03 LTS SP3 riscv64/RVA23; target CI remains required.

## Fixed source and provenance

Official source: <https://cpan.metacpan.org/authors/id/C/CL/CLKAO/IPC-Run-SafeHandles-0.04.tar.gz>.
SHA-256 `8ecd3f85e132ca84a32e6f1b3740d0af6f970591fd2ae69ce813aa7b46eebffc`,
19,431 bytes. Physical bytes match official release metadata and the CLKAO
publisher CHECKSUMS entry. The historical index signature has mathematical
VALIDSIG and an expired signing key tied to the official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`; this is advisory historical evidence,
not a current strong or detached archive signature. Archive SHA-256 is mandatory.

Frozen discovery lineage is Debian stable libipc-run-safehandles-perl 0.04-3
from `discovery-20260808T165000Z-9a89920c269462cd`. No external packaging recipe
was executed. Complete current managed/open-PR aliases and provider module,
RPM and file namespaces were screened before admission.

## License closure and documentation-only patch

Original README and module notices grant Chia-liang Kao's work under Perl terms:
GPL-1.0-or-later OR Artistic-1.0-Perl. Eleven actual bundled build helpers were
individually matched to the exact official Module-Install 0.68 archive, SHA-256
`f6aa0c315cbc9456f642db3de8d2315d658f0a59d46aa0946737fee09d2e293c` (81,319 bytes),
including its Module::AutoInstall 1.03. After removing only POD, line directives
and blank lines, every original code line matches. Module::Install's own
documentation specifically describes inclusion of POD-stripped standard
extensions; this is not a generic assumption that generated code is unlicensed.

`0001-preserve-helper-notices.patch` adds only `BUNDLED-HELPER-NOTICES`: the exact
original per-file attribution/grants and full original distribution LICENSE,
plus provenance labels. Only trailing horizontal whitespace on five license
lines is normalized; the original bytes are retained in the audit evidence and
all license text/terms are unchanged. It restores notices omitted from the bundled stripped
copies, under the same original Perl terms. GNU patch applies it with zero fuzz;
no original executable, source or test file changes. The document is installed
with `%license` and the patch is retained in the SRPM. The unrelated auxiliary
source archive is not a package input or shipped in RPM/SRPM. Remove this patch
only when upstream supplies equivalent complete notices and license text.

## Dependencies, tests and evidence boundary

The target supplies List::MoreUtils, IPC::Run, IPC::Run3, Carp and the original
test/build modules. Runtime dependencies are explicit. The old inc loader is
selected with `perl -I.`; `PERL_AUTOINSTALL=--skipdeps` disables only dependency
downloads, with all dependencies supplied by RPM. It does not select, skip or
alter tests. The manifest declares `network_during_build: false`; this recipe
does not download dependencies, and the verified source enters the build from
the offline cache. This does not assert physical network isolation of CI.

`%check` retains the original complete `make test` target and all four `t/*.t`
files. Test::Pod and Test::Pod::Coverage are explicit target BuildRequires.
Local host execution passed six top-level assertions; the unchanged upstream
optional POD-coverage test naturally skipped because its module is absent on
the host. This is not a zero-skip upstream-suite or target build claim. The
license patch preserves all 20 original source files byte-for-byte. The
installed smoke exercises IPC::Run3 output/error capture both normally and
with the FastCGI role set, then verifies wrapper restoration.

Local source-only, metadata and isolated repository validation/tests/golden are
distinct from approved CI's actual riscv64 build, original target tests, RPM
installation and smoke. No local RPM/QEMU build was performed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

# App::Options 1.12

This proposes official SPADKINS App-Options for openEuler 24.03 LTS SP3,
riscv64/RVA23 with the repository's immutable image. No target build, native,
installed-RPM or publication success is inferred from this preparation.

## Original source and lineage

The authorized/latest/released API identifies the fixed official source
`https://cpan.metacpan.org/authors/id/S/SP/SPADKINS/App-Options-1.12.tar.gz`.
Its 38,921 bytes and SHA-256
`b801a1262101bda8ffab0813f364f0e3b95554cbb6ca7d72509f378fcdaeaa0f`
match both API and publisher CHECKSUMS. All 30 ordinary members/23 files,
complete MANIFEST, original modes (including 02755 directories and 0664
META.yml), examples, helpers and both MakeMaker EXE_FILES remain unpatched
and unrepacked. No source signature verification is claimed.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` canonical
`metacpan.org-release-app-options` contains Debian stable/main
`libapp-options-perl` 1.12-3. Its separate exact inventory key is Ubuntu
resolute/universe 1.12-3, not the same raw lineage row. Both were fetched
2026-08-08T16:50:00Z. These discovery rows do not prove source permission.
Full checksum-bound target primary has neither perl-App-Options nor
perl(App::Options), and supplies the reviewed direct prerequisites, including
undeclared-in-META Date::Format used by retained prefixadmin. This is metadata
availability, not a successful DNF transaction. The updater uses actual official
JSON version/download_url with release_regex null, not a guessed HTML regex.

## Rights and preserved features

The actual grant is in lib/App/Options.pm ACKNOWLEDGEMENTS: copyright 2010
Stephen Adkins, free software under the same terms as Perl. README does not
contain that grant; generated META says unknown and is not its replacement.
The installed original module notice plus complete official Perl v5.38.0
Copying/Artistic texts use `GPL-1.0-or-later OR Artistic-1.0-Perl` accounting.
Those texts are separately pinned to tag-resolved commit
`76298ae68aa7796f0ffc05095b127d23f4b2de8f`, unchanged release-origin notice
supplements, not evidence of Perl code ancestry, an executable dependency,
a relicense or cryptographically verified tag signature. Original copyrights,
CHANGES and all source files remain intact; no general legal-certainty claim.

Both original programs are installed. prefix sources caller-selected shell
configuration and can exec caller commands; prefixadmin can recursively
chmod/chown selected paths. No native privilege, security, administrative,
production or performance validation of these features is claimed. The actual
module has no init method and does not implement the old :none import bypass;
obsolete documentation/benchmark syntax is not copied into the smoke test.
The non-default benchmark is preserved but not run or counted as coverage.

## Complete original default tests

The original MakeMaker default suite is t/main.t and t/old.t. Their active
straight-line Test::More calls are statically 48 and 39, total 87; both use
no_plan and contain no skip/TODO. Actual TAP totals and passing assertions must
still be verified in exact-head hosted CI. Original commented file/pipe/heredoc
comparisons are retained and not counted as coverage. The fixture nonetheless
really executes its cat pipe during parsing, so coreutils is required.

Target check preserves full original make test, then checks full Harness stats
for exactly two files/87 passed assertions and zero skips, TODO, bonus or failures.
Each invocation has a finite 180-second timeout with a 10-second kill-after,
never a retry or failure-to-success translation. It uses fixed ordinary build
UID10001 and a fresh task-specific check_home passed only to child env commands;
shell/global HOME is not exported or repurposed. Child env is otherwise minimal,
so APP_*/PATH_INFO/PREFIX/DOCUMENT_ROOT do not inherit unrelated values. Guards
reject preexisting system/prefix/app test configurations and hostname xyzzy3.
No host configurations are edited/deleted and no original tests are weakened.
The disposable build container and fresh source directory supply isolation.

Default checks concern ordinary option/env/file/hostname parsing, not native
kernel/hardware, privileged CLI behavior, benchmarking or general process security.
No upstream source or target tools have been executed locally.

## Installed smoke boundary

Three fail-closed smoke assertions verify version/provider/original module and
full notices, retained executable presence and CLI module prerequisites, actual
new/read_options defaults, private configuration/file/conditional/substitution/
cat-pipe behavior and invalid argument rejection. Empty import suppresses automatic
configuration discovery only in smoke; the original full default tests still use
normal imports. Smoke never runs prefixadmin's fix/chown or sources a caller's
prefixrc, and does not validate SSH/privileged/native/security behavior. No public
RPM/SRPM URL is inferred from a pull-request artifact.

Installed CLI checks bind the original bytes after the first line separately
from their intended bash or perl-with-warnings interpreter. A shebang-only
installation rewrite must be separately inspected if CI reports one; no broader
program rewrite is accepted and no privileged program is executed by smoke.

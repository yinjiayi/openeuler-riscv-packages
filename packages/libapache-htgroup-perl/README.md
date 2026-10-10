# Apache::Htgroup 1.23

This package targets openEuler 24.03 LTS SP3 riscv64/RVA23 with an unprivileged,
network-enabled QEMU user build. Active update metadata is not target acceptance;
exact-head hosted build and physical RPM/SRPM evidence remain required.
The canonical frozen component is `metacpan.org-release-apache-htgroup` with
Debian stable/main `libapache-htgroup-perl` 1.23-4; the inventory also retains
a separate Ubuntu resolute/universe 1.23-4 row. Upstream is the authorized RBOW
stable release 1.23, not a distribution package archive.

Source0 is the complete original 11,584-byte archive, SHA256
`915ddf0d60c7889f417646a6f998c264626336306b906e3a7e21d25eaafb986c`.
Its publisher CHECKSUMS and authorized API agree. All 15 ordinary safe members,
11 original files/modes, MANIFEST, four tests and groupfile fixture are retained;
no patch, repack, fixture deletion, signature verification or source execution.

Rich Bowen's 2001 copyright and same-Perl grant appear in the module and README.
The whole LICENSE explicitly allows GPL version1-or-later or the Artistic License;
its embedded GPL text is version2, and Artistic text has the generic nine clauses,
not the ten-clause Perl variant. This package distributes under Artistic-1.0
as one original alternative, without removing any upstream choice or relicensing.
Install unchanged LICENSE, README and a copy of the full module as `%license`
so all actual grants/notices survive nodocs. No legal certainty or complete
historical authorship claim is made.

Default MakeMaker selects all four `t/*.t` files with fixed plans 1+4+3+3=11.
No default skip/TODO was observed. The unmodified original `make test` remains,
followed by one bounded explicit target Test::Harness3.48 repeat requiring exact
basenames, four successful files, eleven planned/passed assertions and zero
skip/TODO/bonus/failure totals with an empty failed-file map. Target Test.pm1.31
prints numbered assertions and plans, but its plain exit alone is not a TAP
pass. Harness handles parse errors, actual failure and child exit; this gate
does not regex-parse Console summary wrappers. No runtime suite result exists yet.
The scratch test creates `t/test1.acl` in a fresh writable private BUILD. Only
the original eleven input files are source-integrity comparison inputs; that
generated scratch output is not an upstream source change. Keep fixtures intact.

The module explicitly is not mod_perl; no Apache server is required or started.
The `docs` postamble's cvs2cl command is not a normal build/test target. Runtime
core strict/vars and default Test/MakeMaker, Harness plus packaging and
private-smoke tools are available in the bound official18503/public1192 metadata;
this is not a DNF installation or automatic version-Provide proof. The Revision
expression statically identifies1.23; actual RPM `perl(Apache::Htgroup)=1.23`
still requires hosted product evidence.

Installed smoke uses a fixed nonzero10001 identity using declared util-linux setpriv
and cleared groups, private File::Temp storage only, installed module/notice hash
and version/provider checks. It covers new/add/delete-user/delete-group/save,
load/reload existing-file persistence, empty group preservation and missing-file
error propagation. No system Apache files are touched. Source reload behavior is
used as-is: changes are saved before existing-file reload; no assumption that
reload removes all unsaved members. File locking, atomic saves, malformed-file
safety, daemon behavior, privilege/security, native timing and performance are
not established by these tests or smoke.

Acceptance gates: final six-file review and repository validation/golden/
dashboard/source checksum-only gates, renewed ownership/auth/main leases, then
hosted-only exact-head CI and physical products. Original tests must pass before
installed smoke evidence is accepted. Protected main merge/publication remains
independently trust-gated.

# Test::Deep::UnorderedPairs

The official ETHER CPAN release 0.006 is pinned to SHA-256
`9d6911a9c69b22a26cad198032e6445cfd2a9d6cec4fc3d8a7ca9b965525ccc5` and checked against the PAUSE-signed publisher checksum.
Frozen lineage: Debian stable and Ubuntu resolute, both 0.006-3.

Keep the original MakeMaker `t/*.t` set and all assertions. The scoped
`PERL5LIB="$PWD"` resolves only the release-root relative prerequisite fixture
on modern Perl; it does not alter source or tests. The original defaults cover
comparison diagnostics and repeated keys. The shipped `xt/` author/release
suite is retained as source and is not in the upstream default harness.

The original LICENCE preserves Karen Etheridge's Perl 5 terms. The release
metadata and exact generator archives identify the following rendered-file
donors. Full corresponding copyright and license texts are pinned in
`sources.yaml`, kept in the SRPM, and installed in the binary:

- `Dist-Zilla-6.008.LICENSE`
- `Dist-Zilla-Plugin-Test-ReportPrereqs-0.025.LICENSE`
- `Dist-Zilla-Plugin-InstallGuide-1.200007.LICENSE`
- `Dist-Zilla-PluginBundle-Author-ETHER-0.121.LICENCE`
- `Dist-Zilla-Plugin-Test-CPAN-Changes-0.012.LICENSE`
- `Dist-Zilla-Plugin-Test-CleanNamespaces-0.006.LICENSE`
- `Dist-Zilla-Plugin-Test-Compile-2.056.LICENCE`
- `Dist-Zilla-Plugin-Test-EOL-0.19.LICENCE`
- `Dist-Zilla-Plugin-Test-Kwalitee-2.12.LICENSE`
- `Dist-Zilla-Plugin-MojibakeTests-0.8.LICENSE`
- `Dist-Zilla-Plugin-Test-NoTabs-0.15.LICENSE`
- `Dist-Zilla-Plugin-Test-Pod-No404s-1.003.LICENSE`
- `Dist-Zilla-Plugin-Test-PodSpelling-2.007004.LICENCE`
- `Dist-Zilla-Plugin-Test-Portability-2.001000.LICENSE`
- `Dist-Zilla-Plugin-Test-MinimumVersion-2.000007.LICENSE`
- `Dist-Zilla-Plugin-Test-Synopsis-2.000007.LICENSE`
- `Dist-Zilla-Plugin-CheckChangesHasContent-0.010.LICENSE`

No external distribution recipe or generator was executed. No patch or
network during build. The CI target is openEuler 24.03 LTS SP3 riscv64/RVA23.

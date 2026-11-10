# Test::EOL

This recipe packages the fixed upstream Test::EOL 2.02 CPAN release as
`perl-test-eol` on openEuler 24.03 LTS SP3 RISC-V. Test::EOL checks line
endings and optionally trailing whitespace. The installed module is pure Perl.

- Source: [CPAN Test-EOL-2.02.tar.gz](https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-EOL-2.02.tar.gz).
- SHA-256: `283199d7fb27807fe2226af7b12571c6dc2508d8e5c0feb505d089d31720afc4`;
  matched the CPAN publisher CHECKSUMS and MetaCPAN release metadata.
- License: upstream `LICENCE` is installed unchanged; Perl terms allow
  GPL-1.0-or-later or Artistic-1.0-Perl.
- Build: released MakeMaker recipe with vendor paths and no RISC-V patch.
  The stock default `make test TEST_VERBOSE=1` runs `t/*.t` unmodified;
  upstream author/release suites under `xt/` are not part of that default.
- Installed smoke: call the installed module to check a temporary LF fixture.

Host original tests and staged smoke are preliminary evidence. Target RPM,
DNF install, and functional acceptance require exact-head hosted CI.

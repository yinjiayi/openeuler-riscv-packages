# Test::Is

- Canonical directory: `libtest-is-perl`; RPM: `perl-test-is`.
- Fixed official release: [DOLMEN/Test-Is-20140823.1](https://metacpan.org/release/DOLMEN/Test-Is-20140823.1).
- SHA-256: `fb9a959b7004d629f20d45c9965de59e80f46ab50453906bd1a97ff656419dbe`, matched to the publisher metadata and historically signed PAUSE CHECKSUMS.
- Debian stable, Ubuntu resolute and Fedora source metadata supply discovery lineage, not package recipes.
- Preserve the original Perl 5 grant and complete exact generator licenses: Dist::Zilla 5.020 (MakeMaker, README, POD syntax); Test::Compile 2.043; ReportVersions::Tiny 1.10. Generated members and license bytes were matched to those fixed official releases.
- Original MakeMaker defaults include all 11 test files. The TAP Harness and file formatter are explicit target build requirements so the nested eight-scenario simulation is exercised. No test source or harness condition is changed; release defaults retain their original condition-dependent skips.
- Installed smoke verifies that the module both runs an ordinary condition and emits its original skip protocol for a noninteractive context. The local Perl run is not RISC-V RPM or installation evidence.

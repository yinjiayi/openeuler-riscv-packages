# patchutils

This directory packages patchutils 0.4.5 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, Debian stable, Fedora 44, openSUSE Tumbleweed, and Ubuntu
26.04 LTS. No distribution packaging content was executed.

The official project page points to the signed stable-release directory,
where 0.4.5 is the newest archive. Independent retrieval produced the SHA-256
in `sources.yaml`; inspection found one `patchutils-0.4.5/` root, no unsafe
paths, and GPL-2.0-or-later program headers with the accompanying license.

The RPM enables PCRE2 support and retains the complete upstream Automake
regression suite. Its installed smoke test exercises patch listing and
filtering with fixed local input. Source retrieval is the only networked
phase.

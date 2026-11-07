<!-- SPDX-License-Identifier: Apache-2.0 -->
# dte

This directory packages upstream `https://craigbarnes.gitlab.io/dte/` version `1.11.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and discovery

The official fixed archive is `https://craigbarnes.gitlab.io/dist/dte/dte-1.11.1.tar.gz`,
SHA-256 `3d7d0d375fd31906ed436de20161dddc42d97f969a93d22b02aecfc3451e6c39`.
It matches the upstream `dte-sha256sums.txt` manifest and the official GitHub
release mirror. Required detached-signature verification uses the committed
release key with fingerprint `A3FB922E15870DA250D9DCE1FBCC7A6B0330BEB4`,
published at `https://craigbarnes.gitlab.io/pubkey/0330BEB4.asc`. The trust root
is the upstream HTTPS publication, not independent identity attestation.
The archive's LICENSE, README and source SPDX notices establish GPL-2.0-only.

Discovery lineage is retained from the frozen Debian and Ubuntu rows in
`discovery-20260808T165000Z-9a89920c269462cd`; the release and license were
independently rechecked on 2026-11-06. No stale AUR recipe was executed or used
as source authority. Current canonical packages and all open PRs were screened
for duplicate identity. Official and supplemental target provider/file indexes
contained no dte package, capability or installed-file namespace collision.

## Recipe and tests

The release uses GNU make (target version 4.4.1) and GCC, not Autoconf.
Build dependencies come from the locked openEuler repositories; glibc supplies
iconv, and util-linux supplies setsid for the original Linux CLI test.
No bundled configuration, syntax feature or default test is disabled.
Released man pages are installed directly, so Pandoc is not a build dependency.
The build itself needs no network after the verified source retrieval.

`%check` runs the complete upstream default `make check` target, comprising
the C unit/integration suite and `test/check-opts.sh`. The installation smoke
test checks the installed version, built-in configuration/syntax extraction,
syntax validation and installed data files without requiring an interactive TTY.
Neither this smoke test nor QEMU establishes native hardware/performance behavior.

The first target run, `42152231559` at head
`2d9a5d349e218cfc9eec67b3c54e7dd7b28f4dbe`, passed RPM build and the original
default tests, then installed the RPM successfully but failed this package's
syntax smoke check with exit 65. The exported file was incorrectly named
`syntax`: upstream `load_syntax_file()` resolves the default syntax using the
file's basename, while the exported configuration declares `syntax dte`.
The smoke test now preserves basename `dte`, matching upstream's
`test/check-opts.sh`, and requires a positive loaded-syntax result. No default
test or syntax capability is disabled; the repaired head requires fresh CI.

## Patch and validation boundary

`0001-preserve-dangling-symlink-targets.patch` is a GPL-2.0-only downstream
adaptation of upstream commit `ad39f88ba7cb10b209be1b935250186c968565b1`.
In 1.11.1, `path_absolute()` mistakes a dangling symlink for a new file path.
The patch resolves relative targets against the link's containing directory,
follows further links, retains realpath's error handling and rejects truncation.
It adds relative/absolute dangling target, chain and loop cases to the existing
upstream test function without replacing or dropping any original tests.
Remove it when an upstream release passes these cases without the patch.
This is a generic source correctness fix, not a claimed RISC-V-specific fix;
no upstream write was performed.

A focused host C harness on macOS/arm64 exercised nine path cases: existing
file, new leaf, existing link, relative dangling link, nested relative dangling
link, absolute dangling link, dangling chain, symlink loop and missing parent.
The unmodified release failed four cases; the patched function passed all nine.
These nine host cases are **not** the full original suite or target build proof.
The local host has GNU make 3.81, below upstream's required make version; the
complete default tests remain enabled for approved target CI. Source-only
verification and repository validation also do not prove RPM build/install
success. No local RPM/QEMU build was run; target status for each new head remains
unknown until its own CI completes.

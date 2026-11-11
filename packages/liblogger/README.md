<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblogger

Package the official shinmorisawa/liblogger stable v0.0.3 for openEuler
24.03 LTS SP3 riscv64/RVA23. The tag resolves to commit
`1d68301a3288d5bd0ca49e9edf00f85184583e01`, tree
`0e0a3c7ecc6539822f65a0732645dfcb3eb7d7c0`. All 11 regular archive files
match authenticated Git blob identities; archive SHA-256 is
`65c410cc2b5dfc3a6d74a2ec04e2c5b842cc9b95b395ae3157d38a4e5cc2ff31`.
The discovery snapshot previously lacked a pinned official archive; this
identity/digest review supplies that missing evidence, without executing AUR.
No upstream source signature is supplied; HTTPS/Git/digest verification is
not a signature claim.

## Build, dependencies and namespace

Preserve the original Meson shared/static targets and installed header path;
no patches, feature disabling or substituted implementations. The shared
library retains upstream's unversioned filename `liblogger.so`; runtime owns it,
devel owns the header and replay sources, and static owns the archive. No
new ABI version or pkg-config interface is invented. The prebuilt example
`app/app` stays inert in the original source archive and is never executed
or installed. The example Makefile is not a default build/test target.

Fresh complete official (18,503) and supplemental (1,256) primary/filelists
records contain no conflicting package/capability, library or public header
path. Build dependencies close in the metadata capability walk. This does
not prove DNF SAT resolution or successful installation; hosted CI must do
both with the locked target image and no network during build.

## Tests and license

This release registers zero original Meson tests. Keep `meson test` and the
complete default build; do not describe a zero-test invocation as a suite.
A **downstream logging contract** is the separate packaging fixture which
compiles against staged/installed public headers and both real shared and
static libraries. It checks all seven levels and repeated-level branches,
console/file output, color and splash modes, plain console, append retention,
version, and missing/unopenable filename error results. These checks do not
establish concurrency, thread safety, security, Unicode completeness or
performance. They deliberately use initialized options rather than executing
the unchecked prebuilt example. Installed smoke first requires clean `rpm -V`
results and then repeats the same consumers. No failures or checks are ignored.

Retain the complete MIT grant and Shin Morisawa copyright from `LICENSE`.
The separately authored packaging fixture is Apache-2.0 and includes the
complete pinned official Apache license; this does not relicense upstream.
Local validation is restricted to source/hash review, syntax, metadata and
trusted tooling. Exact-head hosted build, install, smoke and physical
RPM/SRPM acceptance remain required. Submission is not target success,
Auto-merge, merge, native validation or public publication.

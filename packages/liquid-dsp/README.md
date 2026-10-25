# liquid-dsp 1.8.3 — review draft, not submitted

The official signed v1.8.3 annotated tag resolves to
`10041f70cebbe3b97887e75bb41e48b73dda1b23`. All 1,012 source files,
archive executable modes, and the current publisher tag/commit signatures have
been independently rechecked without configuring or executing upstream code.

Preserve all sixteen original CMake option defaults: shared library, examples,
autotests, benchmark construction, FFTW discovery, threads, and SIMD discovery
stay enabled; the originally disabled static library, sandbox, documentation,
coverage, and strict mode stay at their original defaults. Use relative
GNUInstallDirs `lib64`/`include` destinations, preserving relocatable original
`liquid::liquid` CMake exports and `liquid-dsp.pc`. No benchmark timings or
performance claims are produced. Packaging disables embedded build-directory
RPATHs, not a library feature; the original build-tree CTest run receives its
exact build library via `LD_LIBRARY_PATH`, the staged run receives its staged
library, and installed programs use the ordinary system loader paths.

Target checks must run the original unfiltered 192 registered CTest programs
(191 examples plus the complete `xautotest`). The installed tests package must
repeat the same unchanged 191 example binaries and all 1,349 original registry
entries, retaining the raw logs, return codes, registry names, JSON check counts,
and zero-skip summary. The separate downstream C consumer checks matching
headers/library, a known FFT impulse result, and CRC corruption detection through
both pkg-config and the original installed CMake target. These extra checks are
not presented as upstream tests.

Liquid's original code is MIT. Default FFTW linkage is preserved, not disabled
to avoid its GPL-2.0-or-later distribution obligations. The source manifest
carries the exact official `fftw-3.3.10-3.oe2403sp3.src.rpm`, matched by the
official binary providers' SOURCERPM/NEVRA and fixed source-repository checksum.
Its full 3,500-file original archive (including preferred `genfft` source),
original recipe, both patches and original notices are retained. The full RPM
is also physically installed with the runtime, not merely referenced externally.
Default-linked FFTW runtime/development dependencies are pinned to that exact
version/release. There
is no claimed written offer and no mutable-link substitute for source. Full
GPL-2.0 and GPL-3.0 texts accompany the sources and installed license notices.

Original source-only auxiliaries retain their distinct notices: the four
`ax_*` compiler/architecture macros use GPL-3.0-or-later with their Autoconf
macro exception; `config.guess`/`config.sub` retain their GPL-3.0-or-later and
Autoconf-generated-configuration exception; `ax_ext.m4` retains its separate
permissive notice; `install-sh` retains its X Consortium notice and the stated
FSF public-domain changes. These auxiliary notices are not misattributed to
every compiled Liquid binary. The source SRPM and all full texts remain
available with the resulting Liquid source package.

The SPEC/package license expression is the aggregate source-distribution set:
MIT, GPL-2.0-or-later, GPL-3.0-or-later WITH Autoconf-exception-macro for the four
compiler macros, GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 for the two
GNU config scripts, X11 for install-sh, and FSFAP for ax_ext.m4. This aggregate
does not assert that the CMake-built library or its examples contain GPL3
Autoconf code. Liquid's original runtime is MIT; the default linked combination
also carries the FFTW GPL2-or-later distribution obligations. Full original
auxiliary notices and their additional permissions are preserved, not replaced
by these labels. The exception/notice identifiers were compared with the
normative SPDX texts (Autoconf-exception-macro, Autoconf-exception-generic-3.0,
X11 and FSFAP), rather than guessed from filenames.

Current publisher signatures of Liquid's official Git tag and commit were
independently accepted. The vendor FFTW source RPM's actually present OpenPGP
tag 268 (main header only) was independently accepted with current official
openEuler release key fingerprint 8AA16BF9F2CA5244010DCA963B477C60B675600B.
The key is authenticated by the official release HTTPS endpoint, not a separate
third-party fingerprint attestation. No payload OpenPGP signature is present;
the complete SRPM is separately bound by the official source-primary SHA256
and its payload file digests. These checksums are not claimed as a payload
signature. The manifest's null detached-signature field does not mean the
embedded RPM signature was absent or skipped. The SRPM source header's build-host
architecture is `aarch64`; RPM source lead/source-package flag and official
metadata classify this as a source RPM, not an AArch64 target binary.

Current exact main/catalog and all 1,862 open PR file sets have no Liquid DSP
package. The unrelated `mogenslund/liquid` catalog component is not treated as
the same DSP library; broad installed-name collision checks are still retained.

Pending: final version-qualified provider/namespace admission;
inert final QA materialization and isolated trusted tooling/schema/
golden/source-only validation; hosted target build/install and physical RPM/SRPM
acceptance. No local upstream, target, RPM or QEMU execution has occurred.

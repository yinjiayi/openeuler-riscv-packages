<!-- SPDX-License-Identifier: Apache-2.0 -->
# libkmip 0.2.0

Official OpenKMIP/libkmip v0.2.0 resolves to commit
`5b4e6733215f5f2df0d83a761986c973d7c2abf7`. Its fixed HTTPS archive has SHA-256
`42e663a339c2185525880d43a30bc2668aee8251620ca955901107e92d48f378`.
Every one of its 31 archive files matches the complete official Git tree; there
are no gitlinks, archive links, or bundled external sources. Frozen AUR and
openSUSE discovery lineage is retained but neither recipe is executed.

LICENSE explicitly offers Apache-2.0 OR BSD-3-Clause. All C/header notices agree;
all three original license files are installed. This overrides the frozen AUR
AND expression with reviewed original legal evidence. No signature is supplied.

Original defaults build shared AND static libraries, all three OpenSSL example
clients and the whole encoding/decoding test executable. `make test` is unchanged.
The package-only Makefile patch adds overridable LIBDIR (same upstream default),
the missing SONAME symlink, and existing linker/OpenSSL flags on the shared link.
All 178 original registered tests remain enabled; no C source, test body,
registration, assertion, feature or default test changes.
Remove the patch when upstream supports this layout. Original source, headers,
demos, test executable and RST docs remain installed; HTML/Sphinx is not a default.

The installed runner reruns the original binary, rebuilds the entire tests.c
against installed headers/shared library, checks two independent shared/static
consumers (exact integer TTLV bytes, decoded value, memory-clearing API and an
OpenSSL memory BIO), and exercises three demo help paths without a server.
Live remote KMIP operations, server interoperability, cryptographic correctness,
optimized memory-erasure security or certification are not claimed. Upstream's
security warning is retained in original installed docs. [OpenSSL 3.0 BIO docs](https://docs.openssl.org/3.0/man3/BIO_f_ssl/)
and [TLS method docs](https://docs.openssl.org/3.0/man3/SSL_CTX_new/) still document
the APIs used; actual target compilation/link/runtime remains the hosted gate.

Full official/current supplemental primary/filelists joins cover dependency and
exact/casefold/prefix namespace occupancy; non-EQ bounds still require target DNF.
Build networking is disabled; no dependency is fetched by Make. Local checks are
metadata/source/tooling only, never RPM/QEMU/upstream execution. Exact-head hosted
CI and physical RPM/SRPM acceptance must pass before a separate maintainer merge.

# Libkeccak

Official libkeccak 1.4.3 implements the Keccak family, SHA-3, SHAKE and cSHAKE, with bit-oriented inputs, state serialization and HMAC interfaces. Its upstream portable C configuration is retained without architecture patches or disabled features. The complete ISC notice covers the original source archive and is shipped in each explicit subpackage.

The recipe preserves upstream make all, including benchmark compilation, and the original unfiltered make check with its checksum-bound .testfile. Benchmark execution is a separate non-default target and is not requested. All eight original driver groups remain: hexadecimal coding, state operations, digest vectors, bit inputs, truncated outputs, updates, squeeze operations and file hashing. HMAC code is built, but this does not claim HMAC coverage beyond the original driver.

The tests subpackage retains the entire original archive. Staged and normally installed shared/static replays compile the unchanged original test.c, verify the fixture and compare all ten installed public headers with their originals. Upstream squeeze cases print Fail without forwarding their helper return value; additional replay log assertions reject Fail while retaining the original driver, vectors and all default invocations.

Only buildroot /usr/lib is relocated to openEuler lib64. No local source, RPM or QEMU build is performed. Repository tooling validation is not target build/install or physical-product acceptance; those remain CI and merge gates. No security, native-hardware or performance claim is made.

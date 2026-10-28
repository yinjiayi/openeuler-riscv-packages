concurrentqueue 1.0.5: header SDK and target validation

This recipe describes the exact SDK, source grants and required validation.
Admission authority is a separate hash-bound root decision, not this document.
The official fixed v1.0.5 source commit is
9afb99746f0f5fc94ac8aef737053ae0481ba8d1; its 1,567,911-byte archive SHA-256 is
a92a695bc51ab237b1a86acfca66c7424edcd0d96c33a8d2d33864c7a0e142ad.
All 1,830 original regular files and their executable-bit modes are bound to
the fixed Git tree; POSIX write bits may be reduced by the target tar umask.
All original bytes/notices are snapshotted before a single metadata patch.
Only CMakeLists.txt project VERSION 1.0.0 changes to the actual release1.0.5;
no implementation, default, feature, benchmark, unit or fuzz source changes.

Canonical installed SDK outputs are the original three headers and LICENSE.md
under /usr/include/concurrentqueue/moodycamel, plus the original three CMake
exports under /usr/lib64/cmake/concurrentqueue. The upstream CMake INTERFACE
target remains concurrentqueue::concurrentqueue. Consumers use
<moodycamel/concurrentqueue.h> and <moodycamel/blockingconcurrentqueue.h>.
No compiled SDK library, C API library, benchmark or checker is installed as
a development interface. Empty automatic debug subpackages are disabled only
because the installed payload has no ELF, not because build tools lack DWARF.

The original make default tests+benchmarks is built without overriding its
DEBUG_OPTS/RELEASE_OPTS, removing tests or defining NDEBUG for the original
unit target. The unchanged original unit suite runs all45 registrations at
its default8 repetitions with --disable-prompt only. The original infinite
fuzzer cannot finish by definition: its official --seed mode runs100
iterations per executed seed. A fixed sequence of64 full-width seeds is used
in order until actual output covers all6 original categories; every executed
seed must finish successfully. A timeout or incomplete category coverage is
failure, never passing evidence. No throughput benchmark is executed under
QEMU; the original benchmark target is still built and its target ELF checked.
Optional CDSChecker/Relacy verification is separate, not silently claimed run.

Owned target validation is additive: installed/relocated, C++11/C++17 and
direct-GCC/native-CMake form8 positive routes. Every route checks scalar FIFO,
explicit tokens/bulk, concurrent exactly-once delivery, per-producer order
with one consumer, blocking round trips, move-only elements and the semaphore.
It does not impose global cross-producer linearizability. Compiler header
traces and dependency files bind all3 intended SDK headers; compile commands,
target ELF/ABI, linker maps, real runtime library resolutions and RPM-owned
tool/system-header files are recorded. Actual temporary consumer/object ELF
bytes are retained compressed in each route's structured log evidence; system
library bytes are hashed/provider-bound, not redundantly embedded. Every
cached tool/header/library file is rehashed after QA and tool symlinks are
rechecked. CMake consumer compilation is serial
to avoid interleaved -H diagnostics, without changing upstream production
parallelism. Four negative controls require exact nonzero outcomes: missing
header, wrong EXACT CMake version, forced consumer exit23 and no fallback to
the original SDK after hiding a relocated header. The installed payload is
hash/mode-snapshotted before/after; relocated-only mutation is restored and
checked. Raw streams and structured evidence are emitted in CI logs.

License scope is component-specific, not a blanket relicensing of the SDK.
The root Cameron BSD2/BSL alternatives, the separate Preshing2015 semaphore
zlib grant, Preshing2013 hash adaptation BSD3 grant, bundled Boost/dlib BSL,
Intel TBB GPL2 plus its exact additional runtime/template/linking permission,
Relacy BSD3 and revision-specific Ali/KeithB demangle CC BY-SA2.5 material
remain distinct. Owned packaging QA uses Apache2 only. The package License
union inventories those source/notice components; it does not assert every
production header is GPL or CC. Every original file is retained byte-for-byte
as a non-executable full-file source notice, preserving all1,830 notices and
vendored SRPM grants. The additional TBB permission is reproduced verbatim;
no unrelated SPDX exception identifier is substituted. Full CC2.5 legal HTML
and exact revision/author/adaptation attribution accompany the unchanged test
helper; no BSD relicensing of that adaptation is asserted. The Stanford
round-up citation/function remains unchanged. Root bounded engineering review
found no separately material expression beyond its short generic algorithm;
keep every original byte/citation and applicable project notice. No unobserved
public-domain terms, automatic missing-permission finding, judicial warranty
or absent-publisher permission is invented.

The bounded engineering component route remains recorded at SHA-256
0437810ec2058bf5df75c0c7a6b399ec12ce533b6299bf8b6f64a76fecd9713e.
It includes the conservative adapted minitest-file CC2.5 scope in addition
to original notices, not blanket CC/GPL SDK relicensing. The packaged ledger
is descriptive: exact final source/grant/provider/recipe admission must be
held separately in a root decision binding this final manifest and evidence.
Fresh official stable/ref/commit/tree metadata and all1830 Git file identities
were checked. Actual GPG verified the signed Git commit using the current
actual web-flow committer profile public-key offer, full fingerprint
968479A1AFF927E37D1A566BB5690EEEBB952194. GPG TRUST_UNDEFINED is retained:
this proves that offered hosted key's signature, not owner certification,
a personal Cameron authorship signature or an independent archive signature.
The exact archive hash and complete Git byte/mode correlation remain recorded.
The M177 current1934-PR/651-directory/5154-declaration identity fence and all
official/current-publication primary/filelist metadata found no exact native
identity/path conflict for all1857 prospective private and SDK paths. The15
build and9 runtime dependency relations have complete prospective metadata
closure only; actual DNF transaction, target compile/install, provider/header
binding, ABI and physical artifacts remain target acceptance gates.
Twenty Java API-documentation clues, one different-project signing-key
filename and two XGBoost private vendored headers remain scoped lexical clues,
not silently discarded or standalone C++ SDK provider evidence. Exact current
main/open-PR identity and credential guards are rechecked before submission.

Target build/install, complete original suites, all8 owned routes/four
negatives, physical RPM/SRPM and independent main/publication proof remain
unobserved for this recipe. No local upstream/QEMU/RPM build is authorized.

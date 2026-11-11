# libhpptools 1.1.3

Canonical upstream is mateidavid/hpptools, official v1.1.3 at
93bb758cd02cb58b14be80a0f181819d83145af0. The fixed archive SHA-256 is
00474d0875942132dda9e563411a27ae52809966d1cdb8ef5f17ead705b344ae;
all 32 original Git files were compared with the archive. AUR lineage is
discovery evidence only; no AUR recipe is executed. No detached signature
is claimed. Ten headers live under /usr/include/hpptools, not the generic
top-level include namespace. No upstream source or build file is patched.

Root LICENSE is MIT. Bundled examples/catch.hpp has its original BSL-1.0
notice; the full official Boost 1.62.0 companion at fixed commit
4f2bdeb93a4be13ba0dc5e9f44920a2bf67191fc is included with SHA-256
c9bff75738922193e67fa726fa225535870d2aa1059f91452c411736284ad566.
LicenseRef-Public-Domain refers specifically to logsum.hpp's original
Sean Eddy permission statement and Matei David modification notice; it is
not a new blanket license or a claim about all HMMER code. All notices stay.

The original examples/test-alg.make test target runs all nine bundled
Catch TEST_CASEs. The original examples/test-zstr.make test target retains
all 26 plain/gzip/concatenation/nested-gzip/pipe/file/diff commands unchanged.
Both original all targets are built with their original C++11 debug flags;
strict_fstream is an observational example built by all, not an assertion
suite. Original makefiles, sources and headers are hashed before building.
Staged and installed replays verify those hashes, compile in a fresh work
directory against installed headers, and run both original test targets.
Downstream Bash pipefail strengthens failure propagation without replacing
or skipping any original command. Replays are not additional distinct tests.

Header-only noarch payload contains no ELF, but actual locked openEuler
24.03 LTS SP3 riscv64/RVA23 compilation, RPM installation and smoke replay
remain required. System gcc-c++, make, Boost headers and zlib development
files supply the test dependencies, with no network during target build.
Source-only local verification and repository tooling tests do not establish
target build success. Physical RPM/SRPM acceptance is a separate merge gate.
The default suites cover alg and zstr, not every utility or concurrency,
native hardware, timing, performance or security properties. No such claim
is made. No local source/target build or Auto-merge is used.

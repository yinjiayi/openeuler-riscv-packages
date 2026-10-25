# libsoundio

Official stable 2.0.0, commit dc4f84339039ac518b6cd1c0e7683e88e25be470,
fixed codeload SHA-256 a07e692ae236fd196a0e9544499104ff7919ca55b8d0ae9c39c1838c342712c4.
All 49 regular source files were independently bound to official Git blobs.
The complete upstream MIT LICENSE is installed. No source patch is added.
Discovery lineage is retained from the frozen catalog, not used as a recipe
or as evidence for a newer untagged version.

The recipe preserves upstream's default Debug configuration, static/shared
libraries, all four example programs, all five test executables, and Linux
JACK/PulseAudio/ALSA detection. Their development providers are mandatory and
generated configuration must prove all three compiled in. CoreAudio/WASAPI
remain upstream's platform-dependent defaults, not disabled downstream.

`%check` and installed smoke run the unchanged original `unit_tests` executable
without a filter: all six original cases and assertions must pass. The cases
are monotonic-clock sanity, output-stream creation, mirrored memory, nearest
sample rate, basic ring buffer and the original 100000-iteration threaded ring
buffer test. This is not a performance benchmark. The binary embeds private
source objects; its installed replay is not a test against the installed
shared library. Separate downstream C consumers compile/link/run against both
the installed shared library and static archive, verifying versions, compiled
Linux backends, dummy devices/output stream and ring-buffer data. The original
installed `sio_list_devices --backend dummy --short` must report two devices.
Original sources and test/library binary checksums are checked during replay.

Upstream's manual audible playback/recording, device hotplug, server reconnect,
underflow/overflow, USB/raw-device, latency/beep alignment and performance checks
require suitable native RISC-V audio hardware/services and are **unverified**.
Their original programs are built/installed but not falsely counted as passing
automated tests. Dummy-backend checks do not prove these properties. No check,
assertion, backend or default build target is removed or replaced.

Official/supplemental checksum-bound primary/filelists were fully joined;
18 build roots including Linux backend headers have provider closure and no
canonical/provider/SONAME/header/example-path collision. This metadata audit is
not DNF SAT, target build or install proof. CI must still validate the exact
committed head, dependencies, complete default tests, install replay, physical
RPM/SRPMs and immutable source hashes. No local upstream/RPM/QEMU execution,
native-audio proof, auto-merge or public release is claimed.

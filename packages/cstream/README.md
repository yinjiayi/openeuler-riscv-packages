# cstream 4.0.0

The Debian4.0.0-1 source lineage delegates Martin Cracauer's official homepage
and literal fixed HTTPS release archive. Source0 is the unchanged113042-byte
archive, SHA256 `6bc06d7c4386fb98d3a91713434c315d9e6d425c91c886281beaa254c0e096e3`.
Fresh official homepage and complete delegated download index advertise4.0.0;
no signature/key/checksum link was advertised on those two captured pages.
This is a bounded observation, not global absence or permission to skip a
subsequently advertised signature.

The recipe preserves default recursive `all`, `check` and `install`, one C
program and its pregenerated manual. It passes none of the upstream feature
disablers for TCP, sound or resolver. JACK development supply preserves its
default library probe; BSD ossaudio is still probed normally, not force-enabled
or force-disabled. Normal installation does not strip; standard RPM compiler,
linker and debug processing apply. The full30-member original source including
legacy test scripts/logs is retained in SRPM. Upstream comments out its obsolete
`TESTS` assignment, so `make check` has zero enabled cases; we do not reactivate,
trim or count that obsolete script as passing tests.

Two narrow patches retain default functionality: function-lifetime IPv4/IPv6
listener address objects plus initialized `accept` storage; and mode4 polling
of pipe hangup to read EOF and finish draining. Original notices remain. These
are source-level corrections, not broader security or native-platform claims.

Main program/manual use the complete original MIT-style COPYRIGHT. Build-only
generated helpers retain distinct original FSFUL/FSFULLR/X11/public-domain and
GPL2-or-later notices; Source1 adds the complete official GPL2 text for
`auxdir/missing`, which has no distribution exception. None of those helpers is
installed as a runtime executable. The authored tests subpackage is separately
MIT licensed with the complete grant/disclaimer in its script; no full source
archive or helper is installed in that subpackage.

Target-only checks exercise exact CLI/version failures, arbitrary bytes through
all five concurrency modes including EOF, byte limits, generator/sink, private
files/colon paths/fsync, and bounded IPv4/IPv6 loopback listener/client byte
roundtrips. They run against both staged and installed binaries. They are not
benchmarks, audio-device validation, network-isolation proof or native evidence.
Metadata requests `network_during_build:false`; loopback uses no external
endpoint, but actual CI runtime identity/network policy must still be checked.
No upstream program or authored QA was run on the local host.

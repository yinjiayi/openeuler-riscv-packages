# Libabort

Libabort 1.0 provides bounded string operations that call `abort(3)` when the
requested result cannot fit. The full ISC copyright and permission notice is
retained, together with the unchanged official source archive.

Original `make all` builds both libraries and all seven original test drivers;
`make check` executes all seven without filtering. The upstream vsaprintf
driver intentionally does nothing and is documented as covered via saprintf;
seven drivers do not mean seven independent API suites. Functional fork/wait
checks inspect expected SIGABRT or normal exit. They do not establish native
timing, privileged-host behavior or signal-delivery performance. The original
ignored return values for suppressing core dumps remain unchanged.

The tests subpackage retains the checksum-bound whole archive. Staged and
normally installed shared/static replays compile and run every unchanged
original driver, using `-fno-inline` to exercise external library symbols.
The installed public header is compared byte-for-byte. All seven internal
manual aliases remain in their original bounded archive namespace. Only the
staged library directory moves from `/usr/lib` to `/usr/lib64`.

No source patch, disabled feature or local source/RPM/QEMU build is introduced.
Repository validation is not target acceptance: exact-head CI, normal target
installation and actual RPM/SRPM verification are still required before merge.

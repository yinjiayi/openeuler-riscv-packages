# Libhaiku

Libhaiku 2.0.2 returns three-line poetic error messages and prints optional
prefixes for explicit errors or the current errno. The unchanged official
archive and full ISC copyright and permission notice are retained.

Original default `make all` builds both shared and static libraries. Upstream
ships neither a check target nor a test driver; the downstream checks added
here are not an upstream suite. They exercise all four public APIs, specific
errno selection and unknown/negative fallback, three nonempty lines and
stderr prefixes (including NULL and empty prefixes). They run against staged
and normally installed shared/static libraries, with `-fno-inline` exercising
the external inline-wrapper symbol. The original public header is compared
byte-for-byte. Random poem choice, randomness quality, thread safety and
native timing are not established by these functional checks.

No source patch or disabled feature is introduced. Only the installed library
directory moves from `/usr/lib` to `/usr/lib64`. Local validation does not
execute upstream source or target RPM/QEMU builds. Exact-head CI, normal
target installation and physical RPM/SRPM acceptance remain merge gates.

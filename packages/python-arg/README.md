# Python-arg

Installed replay explicitly uses the distribution `/usr` prefix scheme; the
runtime's default `/usr/local` scheme must not misidentify the installed RPM
module. Exact module path, official digest and enabled assertions remain required.

Python-arg 1.0.2 provides the `arg` Python module. The canonical project ID is
`python-arg`; the Python 3 RPM is named `python3-arg`. The fixed official archive
is SHA-256 bound and its complete ISC notice is retained in both binary packages
and the unchanged QA/SRPM archive.

The original no-op default `all` and entire 536-line `test.py` via `make check`
are unchanged. Staged and installed replays use isolated Python with assertions
enabled, prove the loaded module is the installed `arg.py` with the official
source digest, then run the unmodified driver without a source-tree import.
The driver's final usage callback intentionally exits zero; no test is deleted.
The tests subpackage contains the complete checksum-bound official archive.

No source patch or local upstream-source/RPM/QEMU execution. Static admission
and the no-op build are not target test/install acceptance. Exact-head full CI,
ordinary target installation and physical RPM/SRPM acceptance remain merge gates.
Functional parser coverage is not a performance, security or native-RISC-V claim.

# html-xml-utils

This package tracks the official html-xml-utils 8.8 release from W3C. The
RPM build runs the complete upstream Automake test suite and installs the
maintained `hx*`, `asc2xml`, and `xml2asc` command-line utilities.

The libidn and libidn2 development interfaces are present at configure time,
and openEuler's nmap package supplies `nc` for the redirect-limit test. These
capabilities are required for all 172 maintained test cases to run.

The target is openEuler 24.03 LTS SP3 on riscv64/RVA23. The source archive is
pinned by SHA-256. Dependencies and source bytes may be acquired online before
the build; the RPM build itself remains reproducible from the verified inputs.

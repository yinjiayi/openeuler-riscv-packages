# python-text-unidecode

Official Text-Unidecode 1.3 is pinned to formal release commit
`a0005d7a0b43a6aa21ce8a63f1da48c6c44f03e1` and complete Git archive SHA-256
`697939978311e3052d4c584de3fdca7cb23dd744decaa65d283f8400bff8b34b`.
The PyPI 1.3 source distribution was independently compared: shared runtime,
data, tests and license bytes agree; its generated egg-info/setup.cfg tail is
not substituted for the omitted original tox and Travis defaults.

The original LICENSE and README offer the Artistic-1.0-Perl alternative.
This package selects that license, preserves all twelve original Git blobs and
ships the unmodified data.bin. No patch or Perl table regeneration is used.
Discovery lineage is retained from Arch, Debian, Fedora and openSUSE; their
packaging text is not executed or used as official source evidence.

The original Travis script invokes tox; tox.ini runs `py.test []`. The supplied
official target tox 4.11.1 parser explicitly treats `[]` as `{posargs}` and
empty command-line arguments as an empty replacement. The effective original
test default is therefore plain `py.test`, without a selector or skip. The RPM
runs that whole default in `%check` and again against authentic installed
runtime/data files. This is an offline RPM packaging interpretation of tox's
build/install/environment wrapper, not a claim that tox or its historical
Python 2.7/3.4–3.7/PyPy interpreter matrix ran. Target validation uses Python
3.11 only. All original tox/Travis/setup configs remain unchanged and installed.

The original suite has three test functions and 133 statically enumerated
parameter cases. These are source counts, not claimed collected or passed
tests. Installed validation checks full original file SHA-256 values and RPM
ownership, then copies only the unchanged test module to an empty scratch
directory. No source runtime or PYTHONPATH override shadows the installed RPM.

The fixed target is openEuler 24.03 LTS SP3 riscv64/RVA23. The distribution has
no runtime dependencies beyond Python; pytest is included for committed
installed acceptance. Repository schema/golden checks and offline source
verification are separate from target build/install results. No local RPM,
QEMU, upstream backend or default test execution, CI success, or publication
is claimed by this recipe. Target CI must establish full build/install results
and physical RPM/SRPM artifacts before merge or publication.

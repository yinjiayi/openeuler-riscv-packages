<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-natsort

Packages upstream natsort 8.4.0 for openEuler 24.03 LTS SP3, riscv64/RVA23.
MIT remains the source license; Apache-2.0 covers original packaging only.

The fixed official Git commit d9503c08f8f83ce8a89bfcc45fec136868756243 retains all
62 original files, hidden workflows, tests, Unicode tables, documentation and
MIT notice. Its full SHA-256 is f0fdff4da8b535f475eed4b49d1942f787595558983a43a361ce9e68c3378b44.
The formal PyPI 8.4.0 sdist has identical shared files except its generated
setup.cfg egg_info appendix; the unmodified Git default configuration is used.
The frozen python-natsort inventory identity and actual Arch extra 8.4.0-4 row
are discovery provenance, not proof of target supply or a target build.

The original GitHub Tests job explicitly maps Python 3.11 to tox py311 with no
extras. Both buildroot and installed-RPM engines preserve all four commands:
doctest -o IGNORE_EXCEPTION_DETAIL docs/howitworks.rst; pytest README.rst
docs/examples.rst; pytest --doctest-modules on installed natsort; and the entire
pytest --hypothesis-profile=slow-tests --tb=short --cov installed-natsort
--cov-report term-missing suite, followed by original coverage xml. No selectors,
filters, new skips, source edits, coverage thresholds or feature disabling are
added. Original locale/ICU conditionals and .coveragerc are retained. The official
glibc-all-langpacks supplies the original EN/DE/CZ locale prerequisite. Python
module entrypoints preserve arguments without assuming unversioned coverage CLI.

Each engine uses a fresh copy of every original non-runtime file and unchanged
tests, with no local natsort source directory. An import guard verifies every
natsort module's actual installed origin and original SHA. Installed smoke also
verifies RPM ownership, all 62 original hashes, runtime hashes and source archive;
only explicitly matched RPM-generated Python caches are permitted as extra.
The no-network wheel build uses supplied setuptools/wheel and a fixed reproducible
ZIP timestamp input (1980-01-01), not a source/default modification.

Other original interpreter/OS/extras matrices and separate Python 3.8 formatting,
static/type/package-validation jobs remain retained and unclaimed. The profiling
script is retained but not selected by original pytest defaults; no performance
claim is made. Trusted repository checks and offline source-only verification
are local; RPM/default/buildroot/installed execution belongs solely to real CI.
Target CI success, RPM/SRPM links and publication are unverified at submission.

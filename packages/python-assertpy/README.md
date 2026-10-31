<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-assertpy

This package is official stable assertpy release 1.1 for openEuler24.03LTS-SP3,
riscv64/RVA23. Binary RPM python3-assertpy, distribution/import assertpy;
the catalog's unrelated python-aioswitcher association is not source identity.

Official tag 1.1 maps to b9ad7ee2d673a45f9a5b68c3b7aa2d077560bb7c.
The whole fixed archive SHA-256 is
6b8a12838251d5769544608756641dfb6bcc673e7a326750b117078193358458;
all61 Git blobs, full BSD-3-Clause copyright/permission/disclaimer and complete
tests are retained. No verified source signature is claimed; SHA-256 and the
fixed official Git object identities are the retained source evidence.

Default Travis command is PYTHONPATH=. py.test -v --cov=assertpy
--cov-report term-missing tests. The recipe uses the equivalent target pytest
module driver, retains every30 original test file/604 statically identified
test function (not an executed test count), coverage and configuration, and
repeats the whole suite after installation. The unchanged .coveragerc,
including branch=True and original report omissions, is explicitly RPM-owned
and copied into installed-suite scratch. Nothing is filtered or patched.
Hosted coveralls upload is not claimed as an offline correctness gate.

Travis pins requests2.21 for old Python3.4 compatibility. This Python3.11 target
supplies requests2.31; its physical CaseInsensitiveDict implementation/API was
inspected against the unchanged mapping test, which makes no network request.
Requests is required and explicitly imported before testing, so the upstream
optional absent-requests branch cannot silently stand in for that case.

Source import order was audited before considering a compatibility patch:
assertpy imports inspect before all relative mixins; the physical target
Python3.11.6 inspect module explicitly imports collections.abc. Thus local
collection-ABC lines do not justify an invented target failure or a source
patch. No upstream/backend/default tests were executed locally.

Build uses Python3.11.6, setuptools68, pytest7.4.4, pytest-cov4.1 and requests2.31.
The library has no declared third-party runtime requirements; pytest-cov and
requests are RPM-owned installed-suite support. Canonical provider/namespace
and full dependency closure are checked against immutable supplier inputs;
non-EQ RPM constraints remain subject to real target DNF acceptance.

Installed tests run from clean scratch containing only the unchanged tests and
setup.cfg and .coveragerc, with no source assertpy library/PYTHONPATH shadow; version, imported
library path and every test-file RPM ownership are guarded. No RISC-V patch is
justified. Status stays unknown pending exact-head CI build/install results
and physical RPM/SRPM verification. Repository tests/source-only verification
are not target success.

External sources retain upstream licenses. Apache-2.0 applies only to original
packaging metadata, scripts and documentation.

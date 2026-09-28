<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblinear

LIBLINEAR 2.50 is the current stable release on its official project page.
The official annotated `v250` tag resolves to commit
`491c9f1188b97ba70847c70a68be363d186ddf9d`. Its commit-pinned HTTPS
archive has SHA-256 `ad9c824a631e48fd57fe21ab23e87e9de0413cf0558d0fa9dd89685aec76c185`
and contains only regular files and directories under one source root. The
source `COPYRIGHT` is BSD-3-Clause. Debian metadata is discovery lineage only;
no distribution recipe was read or executed.

This package targets openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It builds
upstream's shared `liblinear.so.6`, public C API, and training/prediction tools
as `liblinear-train` and `liblinear-predict` to avoid generic command names.
The bundled BLAS routines are built as position-independent code. Python and
MATLAB interfaces are outside this initial package scope.

Upstream does not register an automated test suite. `%check` uses its shipped
270-row `heart_scale` sample to train and predict, checks a minimum in-sample
fit and row count, runs five-fold cross-validation, and loads the model through
the shared library API. The installed-RPM smoke test trains and predicts a
two-point fixture through the public API. These are functional tests, not an
independent accuracy benchmark or a performance claim.

Apache-2.0 covers the original packaging metadata, test, and documentation
here; the upstream source retains BSD-3-Clause terms.

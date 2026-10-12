#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblinear liblinear-devel
pkg-config --modversion liblinear | grep -Fx '2.50'
rpm -q --provides liblinear | grep -F 'liblinear.so.6()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat > "$smoke_dir/liblinear-smoke.cpp" <<'EOF'
#include <linear.h>

int main() {
    if (LIBLINEAR_VERSION != 250 || liblinear_version != 250) return 1;
    feature_node positive[] = {{1, 1.0}, {-1, 0.0}};
    feature_node negative[] = {{1, -1.0}, {-1, 0.0}};
    feature_node *samples[] = {positive, negative};
    double labels[] = {1.0, -1.0};
    problem input = {2, 1, labels, samples, -1.0};
    parameter options = {};
    options.solver_type = L2R_L2LOSS_SVC_DUAL;
    options.eps = 0.01;
    options.C = 1.0;
    options.p = 0.1;
    options.regularize_bias = 1;
    if (check_parameter(&input, &options) != nullptr) return 2;
    model *trained = train(&input, &options);
    if (!trained) return 3;
    bool ok = predict(trained, positive) == 1.0 &&
              predict(trained, negative) == -1.0;
    free_and_destroy_model(&trained);
    return ok ? 0 : 4;
}
EOF
read -r -a pkg_flags <<<"$(pkg-config --cflags --libs liblinear)"
c++ "$smoke_dir/liblinear-smoke.cpp" "${pkg_flags[@]}" -o "$smoke_dir/liblinear-smoke"
"$smoke_dir/liblinear-smoke"

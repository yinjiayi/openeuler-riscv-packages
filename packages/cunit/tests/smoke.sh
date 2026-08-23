#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cunit cunit-libs cunit-devel cunit-help
test "$(pkg-config --modversion cunit)" = "2.1-3"

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/cunit-smoke.c" <<'EOF'
#include <CUnit/Basic.h>

static void test_truth(void)
{
    CU_ASSERT(1 == 1);
}

int main(void)
{
    if (CU_initialize_registry() != CUE_SUCCESS) {
        return 1;
    }
    CU_pSuite suite = CU_add_suite("smoke", NULL, NULL);
    if (suite == NULL || CU_add_test(suite, "truth", test_truth) == NULL) {
        CU_cleanup_registry();
        return 1;
    }
    CU_basic_set_mode(CU_BRM_SILENT);
    CU_basic_run_tests();
    unsigned int failures = CU_get_number_of_failures();
    CU_cleanup_registry();
    return failures == 0 ? 0 : 1;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs cunit)"
cc -Wall -Wextra -Werror "$smoke_dir/cunit-smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/cunit-smoke"
"$smoke_dir/cunit-smoke"

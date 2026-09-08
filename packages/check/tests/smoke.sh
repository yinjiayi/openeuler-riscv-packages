#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- check check-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <check.h>

START_TEST(test_target) {
    ck_assert_str_eq("riscv64", "riscv64");
}
END_TEST

int main(void) {
    Suite *suite = suite_create("installed-check");
    TCase *test_case = tcase_create("core");
    SRunner *runner;
    int failed;
    tcase_add_test(test_case, test_target);
    suite_add_tcase(suite, test_case);
    runner = srunner_create(suite);
    srunner_run_all(runner, CK_NORMAL);
    failed = srunner_ntests_failed(runner);
    srunner_free(runner);
    return failed == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs check) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

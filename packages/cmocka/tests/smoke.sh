#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcmocka libcmocka-devel
test "$(pkg-config --modversion cmocka)" = 2.0.2
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cmocka.h>

static void test_smoke(void **state)
{
    (void)state;
    assert_true(1);
}

int main(void)
{
    const struct CMUnitTest tests[] = {cmocka_unit_test(test_smoke)};
    return cmocka_run_group_tests(tests, NULL, NULL);
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs cmocka)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

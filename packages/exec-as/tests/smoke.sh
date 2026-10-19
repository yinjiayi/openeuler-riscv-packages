#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    tool="$root/usr/bin/exec-as"
    archive="$root/usr/share/exec-as/qa/exec-as-1.2.3.tar.gz"
    echo '3813e2975216e3c332d69e6d9ff118efbf65eb3cabc87ea50cf33079540c5d44  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cd "$work"
    gcc -std=c99 -O2 -g -Wall -Wextra test.c -o original-test
    test "$("$tool" ./original-test 1 2 3)" = '1,3'
    test "$("$tool" ./original-test 'custom name' '' 'a b')" = 'custom name,3'
    test "$(PATH="$work:/usr/bin:/bin" "$tool" original-test custom)" = 'custom,1'
    # Diagnostic input for the unresolved target shell-forwarding failure.
    # Keep the failing assertion below; these observations do not waive it.
    cat > argv-diagnostic.c <<'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    int i;
    printf("argc=%d\n", argc);
    for (i = 0; i < argc; i++) {
        const unsigned char *p = (const unsigned char *)argv[i];
        printf("argv[%d]=", i);
        for (; *p; p++) printf("%02x", (unsigned int)*p);
        putchar('\n');
    }
    return getenv("EXEC_AS_DIAGNOSTIC_EXIT") ? 23 : 0;
}
EOF
    gcc -std=c99 -O2 -g -Wall -Wextra argv-diagnostic.c -o argv-diagnostic
    "$tool" ./argv-diagnostic custom -c 'printf "%s,%s\n" "$0" "$1"' 'two words'
    "$tool" ./argv-diagnostic 'custom name' '' 'a b'
    if EXEC_AS_DIAGNOSTIC_EXIT=1 "$tool" ./argv-diagnostic custom; then actual=0; else actual=$?; fi
    test "$actual" -eq 23
    readlink -f /bin/sh
    /bin/sh -c 'printf "direct shell: %s,%s\n" "$0" "$1"' custom 'two words'
    if "$tool" /bin/sh custom -c 'printf "via exec-as: %s,%s\n" "$0" "$1"' 'two words'; then actual=0; else actual=$?; fi
    printf 'diagnostic shell exit: %s\n' "$actual"
    test "$("$tool" /bin/sh custom -c 'printf "%s,%s\n" "$0" "$1"' 'two words')" = 'custom,two words'
    printf 'not executable\n' > denied
    chmod 600 denied
    expect_status() {
        expected=$1
        shift
        if "$@" > stdout.log 2> stderr.log; then actual=0; else actual=$?; fi
        test "$actual" -eq "$expected"
        test ! -s stdout.log
        test -s stderr.log
    }
    expect_status 125 "$tool"
    expect_status 127 "$tool" "$work/no-such-command" custom
    expect_status 126 "$tool" "$work/denied" custom
    expect_status 126 "$tool" "$work" custom
    if "$tool" /bin/sh custom -c 'exit 23'; then actual=0; else actual=$?; fi
    test "$actual" -eq 23
    echo 'PASS exec-as unchanged original driver, argv/PATH/status/error functional checks'
)
run_installed_tests ''

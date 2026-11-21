#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -f /usr/lib64/libptytty.so.0
test -f /usr/include/libptytty.h
cd /usr/share/licenses/libptytty/license-notices
sha256sum -c SHA256SUMS
cd /usr/libexec/libptytty-tests
sha256sum -c SHA256SUMS
driver=/usr/libexec/libptytty-tests/api-smoke
test -x "$driver"
trace="$(mktemp)"
trap 'rm -f "$trace"' EXIT
run_driver() {
    # RPM installation requires root, but the functional driver must not.
    # Numeric IDs do not depend on an account existing in the minimal image.
    if [[ $EUID -eq 0 ]]; then
        /usr/bin/setpriv --reuid=65534 --regid=65534 --clear-groups \
            /usr/bin/env LD_DEBUG=bindings "$driver"
    else
        LD_DEBUG=bindings "$driver"
    fi
}
if run_driver 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libptytty installed raw loader trace'
cat "$trace"
echo 'END libptytty installed raw loader trace'
sha256sum "$trace"
verify_installed_binding() {
    local trace=$1 expected_driver=$2 expected_library=$3 symbol=$4
    local line caller target observed_symbol found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}
            target=${BASH_REMATCH[2]}
            observed_symbol=${BASH_REMATCH[3]}
            [[ $observed_symbol == "$symbol" ]] || continue
            [[ $caller == /* && $caller -ef $expected_driver ]] || continue
            if [[ $target != /* || ! $target -ef $expected_library ]]; then
                printf 'binding %s: FAIL (target %s is not installed %s)\n' "$symbol" "$target" "$expected_library" >&2
                return 1
            fi
            printf 'binding %s: PASS (target %s is same file as %s)\n' "$symbol" "$target" "$expected_library"
            found=true
        fi
    done < "$trace"
    if [[ $found != true ]]; then
        printf 'binding %s: FAIL (no exact installed-driver symbol binding)\n' "$symbol" >&2
        return 1
    fi
}
for symbol in ptytty_init ptytty_create ptytty_get ptytty_pty ptytty_tty ptytty_set_utf8_mode ptytty_close_tty ptytty_delete; do
    verify_installed_binding "$trace" "$driver" /usr/lib64/libptytty.so.0 "$symbol"
done
echo 'libptytty installed six-case replay and eight library bindings PASS'

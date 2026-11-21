#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libabw-0.1.so.1.0.4
driver=/usr/libexec/libabw-tests/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/include/libabw-0.1/libabw/libabw.h
cd /usr/share/licenses/libabw/license-notices
test "$(wc -l < SHA256SUMS)" -eq 99
sha256sum -c SHA256SUMS
cd /usr/libexec/libabw-tests
sha256sum -c SHA256SUMS
trace="$(mktemp)"
trap 'rm -f "$trace"' EXIT
if LD_DEBUG=bindings "$driver" 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libabw installed raw loader trace'
cat "$trace"
echo 'END libabw installed raw loader trace'
sha256sum "$trace"
verify_installed_binding() {
    local symbol=$1 line caller target observed found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}
            target=${BASH_REMATCH[2]}
            observed=${BASH_REMATCH[3]}
            [[ $observed == "$symbol" ]] || continue
            [[ $caller == /* && $caller -ef $driver ]] || continue
            if [[ $target != /* || ! $target -ef $library ]]; then
                printf 'binding %s: FAIL target=%s\n' "$symbol" "$target" >&2
                return 1
            fi
            printf 'binding %s: PASS target=%s same installed file\n' "$symbol" "$target"
            found=true
        fi
    done < "$trace"
    [[ $found == true ]] || { printf 'missing exact driver binding: %s\n' "$symbol" >&2; return 1; }
}
verify_installed_binding _ZN6libabw11AbiDocument21isFileFormatSupportedEPN10librevenge15RVNGInputStreamE
verify_installed_binding _ZN6libabw11AbiDocument5parseEPN10librevenge15RVNGInputStreamEPNS1_17RVNGTextInterfaceE
test "$(/usr/bin/abw2text --version)" = 'abw2text 0.1.4'
test "$(/usr/bin/abw2html --version)" = 'abw2html 0.1.4'
test "$(/usr/bin/abw2raw --version)" = 'abw2raw 0.1.4'
cli_text="$(/usr/bin/abw2text simple.abw)"
printf '%s\n' "$cli_text" | grep -F 'libabw package streaming roundtrip'
test -s /usr/share/doc/libabw/html/index.html
echo 'libabw installed six-case replay, two exact API bindings and CLI parsing PASS'

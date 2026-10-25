#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- termox
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
for p in /usr/lib64/libTermOx.a /usr/lib64/termox/libescape.a /usr/share/termox-tests/api-smoke.cpp /usr/libexec/termox/api-smoke /usr/lib64/pkgconfig/termox.pc; do
    test -f "$p"
    test "$(rpm -qf --qf '%{NAME}' -- "$p")" = termox
done
(cd /usr/share/licenses/termox/source-notices; sha256sum -c SHA256SUMS)
sha256sum /usr/lib64/libTermOx.a /usr/lib64/termox/libescape.a > "$tmp/archives.before"
cat > "$tmp/expected.stdout" <<'TERMOX_EXPECTED_EOF'
TERMOX_API_CASE_1 construct-and-fill PASS
TERMOX_API_CASE_2 mutable-and-const-index PASS
TERMOX_API_CASE_3 canvas-offset PASS
TERMOX_API_CASE_4 resize-then-fill PASS
TERMOX_API_CASE_5 unicode-and-invalid-input PASS
TERMOX_API_CASE_6 signal-disconnect-and-lifetime PASS
TERMOX_API_TOTAL=6 PASS
TERMOX_EXPECTED_EOF
run_api() {
    local label=$1 status
    shift
    if "$@" > "$tmp/$label.stdout" 2> "$tmp/$label.stderr"; then
        status=0
    else
        status=$?
    fi
    cat "$tmp/$label.stdout" "$tmp/$label.stderr"
    test "$status" -eq 0
    test ! -s "$tmp/$label.stderr"
    cmp "$tmp/expected.stdout" "$tmp/$label.stdout"
}
run_api installed-driver /usr/libexec/termox/api-smoke
read -r -a pcflags <<< "$(pkg-config --cflags --static --libs termox)"
if c++ /usr/share/termox-tests/api-smoke.cpp "${pcflags[@]}" \
    -Wl,-Map="$tmp/consumer.map",--cref -Wl,--trace -o "$tmp/consumer" > "$tmp/link.trace" 2>&1; then
    link_status=0
else
    link_status=$?
fi
cat "$tmp/link.trace"
test "$link_status" -eq 0
cat "$tmp/consumer.map"
# These are target assertions, not an already-observed local archive claim.
# CMake names object members after the exact listed terminal/transcode sources.
ar t /usr/lib64/libTermOx.a > "$tmp/termox.members"
ar t /usr/lib64/termox/libescape.a > "$tmp/escape.members"
cat "$tmp/termox.members" "$tmp/escape.members"
test "$(grep -c -Fx 'terminal.cpp.o' "$tmp/termox.members")" -eq 1
test "$(grep -c -Fx 'transcode.cpp.o' "$tmp/escape.members")" -eq 1
grep -E '^/usr/lib64/libTermOx[.]a\(terminal[.]cpp[.]o\)' "$tmp/consumer.map"
grep -E '^/usr/lib64/termox/libescape[.]a\(transcode[.]cpp[.]o\)' "$tmp/consumer.map"
nm -C -A --defined-only /usr/lib64/libTermOx.a /usr/lib64/termox/libescape.a > "$tmp/archives.nm"
nm -C --defined-only "$tmp/consumer" > "$tmp/consumer.nm"
cat "$tmp/archives.nm" "$tmp/consumer.nm"
grep -E '^/usr/lib64/libTermOx[.]a:terminal[.]cpp[.]o:.* T ox::ScreenBuffer::' "$tmp/archives.nm"
grep -E '^/usr/lib64/termox/libescape[.]a:transcode[.]cpp[.]o:.* T esc::detail::u32_to_u8' "$tmp/archives.nm"
grep -E ' T ox::ScreenBuffer::' "$tmp/consumer.nm"
grep -E ' T esc::detail::u32_to_u8' "$tmp/consumer.nm"
readelf -h /usr/lib64/libTermOx.a /usr/lib64/termox/libescape.a > "$tmp/archives.elf"
cat "$tmp/archives.elf"
test "$(sed -n 's/^[[:space:]]*Machine:[[:space:]]*//p' "$tmp/archives.elf" | LC_ALL=C sort -u)" = RISC-V
readelf -h "$tmp/consumer" > "$tmp/elf-header"
cat "$tmp/elf-header"
grep -E 'Machine:[[:space:]]+RISC-V' "$tmp/elf-header"
run_api installed-consumer "$tmp/consumer"
# A build that omits TermOx must genuinely fail rather than use the build tree.
read -r -a cflags <<< "$(pkg-config --cflags termox)"
read -r -a icuflags <<< "$(pkg-config --libs icu-uc icu-i18n)"
if c++ -std=c++20 /usr/share/termox-tests/api-smoke.cpp "${cflags[@]}" \
    /usr/lib64/termox/libescape.a "${icuflags[@]}" -pthread -o "$tmp/missing-termox" > "$tmp/negative-link.log" 2>&1; then
    cat "$tmp/negative-link.log"
    exit 1
fi
cat "$tmp/negative-link.log"
test ! -e "$tmp/missing-termox"
grep -E 'undefined reference.*ox::(ScreenBuffer|Canvas)' "$tmp/negative-link.log"
sha256sum -c "$tmp/archives.before"
sha256sum "$tmp/"*
printf 'TERMOX_INSTALLED_STATIC_CONSUMER=6 NEGATIVE_LINK=1 PASS\n'

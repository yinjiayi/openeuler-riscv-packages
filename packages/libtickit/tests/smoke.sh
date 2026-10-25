#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtickit
rpm -q -- libtickit-devel
rpm -V -- libtickit libtickit-devel
test "$(rpm -q --qf '%{VERSION}' libtickit)" = '0.4.6'
test "$(rpm -q --qf '%{ARCH}' libtickit)" = 'riscv64'
rpm -q --provides libtickit | grep -F 'libtickit.so.3()(64bit)'
test "$(pkg-config --modversion tickit)" = '0.4.6'
test "$(pkg-config --variable=libdir tickit)" = '/usr/lib64'
test "$(pkg-config --variable=includedir tickit)" = '/usr/include'
test -r /usr/lib64/libtickit.a
test ! -e /usr/lib64/libtickit.la
for header in tickit.h tickit-evloop.h tickit-mockterm.h tickit-termdrv.h; do
    test -r "/usr/include/$header"
    rpm -qf "/usr/include/$header" | grep -E '^libtickit-devel-'
done

mapfile -t manuals < <(rpm -ql libtickit-devel | awk '/\/man[37]\/tickit.*[.][37]([.]gz)?$/')
test "${#manuals[@]}" -eq 245
for manual in "${manuals[@]}"; do
    test -r "$manual"
done

for package in libtickit libtickit-devel; do
    mapfile -t notices < <(rpm -ql "$package" | awk '/\/licenses\/.*\/(LICENSE|unicode[.]h)$/')
    test "${#notices[@]}" -eq 2
    for notice in "${notices[@]}"; do
        case "${notice##*/}" in
            LICENSE) expected='57158b9121412fb765f4e58f953ca0ceacadfff95e2403359b8254e5df487d37' ;;
            unicode.h) expected='7f7c06d9177fa335c285e366ed7ffa1580db88c631aac4409caf2c7163cb4816' ;;
            *) exit 1 ;;
        esac
        test "$(sha256sum -- "$notice" | cut -d ' ' -f 1)" = "$expected"
    done
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat > "$smoke_dir/consumer.c" <<'EOF'
/* SPDX-License-Identifier: Apache-2.0 */
#include <string.h>
#include <tickit.h>
#include <tickit-mockterm.h>

int main(void)
{
    if (TICKIT_VERSION_MAJOR != 0 || TICKIT_VERSION_MINOR != 4 ||
        TICKIT_VERSION_PATCH != 6 || tickit_version_major() != 0 ||
        tickit_version_minor() != 4 || tickit_version_patch() != 6)
        return 1;

    TickitPen *pen = tickit_pen_new();
    TickitPenRGB8 rgb = { .r = 0x12, .g = 0x34, .b = 0x56 }, got;
    if (!pen)
        return 2;
    tickit_pen_set_bool_attr(pen, TICKIT_PEN_BOLD, 1);
    tickit_pen_set_colour_attr(pen, TICKIT_PEN_FG, 1);
    tickit_pen_set_colour_attr_rgb8(pen, TICKIT_PEN_FG, rgb);
    if (!tickit_pen_get_bool_attr(pen, TICKIT_PEN_BOLD) ||
        !tickit_pen_has_attr(pen, TICKIT_PEN_FG) ||
        !tickit_pen_has_colour_attr_rgb8(pen, TICKIT_PEN_FG))
        return 3;
    got = tickit_pen_get_colour_attr_rgb8(pen, TICKIT_PEN_FG);
    if (got.r != rgb.r || got.g != rgb.g || got.b != rgb.b)
        return 3;
    tickit_pen_unref(pen);

    TickitRect a, b, intersection;
    tickit_rect_init_sized(&a, 1, 2, 5, 8);
    tickit_rect_init_sized(&b, 3, 4, 6, 3);
    if (!tickit_rect_intersect(&intersection, &a, &b) ||
        intersection.top != 3 || intersection.left != 4 ||
        intersection.lines != 3 || intersection.cols != 3)
        return 4;
    if (tickit_utf8_mbswidth("A\xe4\xb8\xad") != 3)
        return 5;

    TickitString *string = tickit_string_new("tickit", 6);
    if (!string || tickit_string_len(string) != 6 ||
        memcmp(tickit_string_get(string), "tickit", 6) ||
        tickit_string_ref(string) != string)
        return 6;
    tickit_string_unref(string);
    tickit_string_unref(string);

    TickitTerm *term = tickit_mockterm_new(4, 12);
    TickitRenderBuffer *buffer = tickit_renderbuffer_new(4, 12);
    if (!term || !buffer || tickit_renderbuffer_text_at(buffer, 1, 2, "OK") != 2)
        return 7;
    tickit_renderbuffer_flush_to_term(buffer, term);
    char rendered[8] = {0};
    if (tickit_mockterm_get_display_text(term, rendered, sizeof rendered, 1, 2, 2) != 2 ||
        memcmp(rendered, "OK", 2))
        return 8;

    TickitWindow *root = tickit_window_new_root(term);
    if (!root || tickit_window_get_term(root) != term)
        return 9;
    TickitRect geometry = tickit_window_get_geometry(root);
    if (geometry.top != 0 || geometry.left != 0 ||
        geometry.lines != 4 || geometry.cols != 12)
        return 10;
    tickit_window_unref(root);
    tickit_renderbuffer_unref(buffer);
    tickit_term_unref(term);
    return 0;
}
EOF

read -r -a tickit_cflags <<< "$(pkg-config --cflags tickit)"
read -r -a tickit_libs <<< "$(pkg-config --libs tickit)"
read -r -a dependency_libs <<< "$(pkg-config --libs termkey unibilium)"
cc -std=c99 -Wall -Wextra -Werror "${tickit_cflags[@]}" \
    "$smoke_dir/consumer.c" -o "$smoke_dir/shared-consumer" "${tickit_libs[@]}"
"$smoke_dir/shared-consumer"
cc -std=c99 -Wall -Wextra -Werror "${tickit_cflags[@]}" \
    "$smoke_dir/consumer.c" -o "$smoke_dir/static-consumer" \
    /usr/lib64/libtickit.a "${dependency_libs[@]}"
"$smoke_dir/static-consumer"

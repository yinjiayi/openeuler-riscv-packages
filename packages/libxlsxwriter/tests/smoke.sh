#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxlsxwriter libxlsxwriter-devel
pkg-config --modversion xlsxwriter | grep -Fx '1.2.4'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libxlsxwriter-smoke.c" <<'EOF'
#include <string.h>
#include <xlsxwriter.h>

int main(int argc, char **argv) {
    lxw_workbook *workbook;
    lxw_worksheet *worksheet;

    if (argc != 2 || strcmp(lxw_version(), "1.2.4") != 0)
        return 1;
    workbook = workbook_new(argv[1]);
    if (workbook == NULL)
        return 2;
    worksheet = workbook_add_worksheet(workbook, "RVA23");
    if (worksheet == NULL) {
        workbook_close(workbook);
        return 3;
    }
    if (worksheet_write_string(worksheet, 0, 0, "openEuler", NULL) !=
            LXW_NO_ERROR ||
        worksheet_write_number(worksheet, 1, 0, 1.2, NULL) != LXW_NO_ERROR) {
        workbook_close(workbook);
        return 4;
    }
    return workbook_close(workbook) == LXW_NO_ERROR ? 0 : 5;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs xlsxwriter)"
cc "$smoke_dir/libxlsxwriter-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libxlsxwriter-smoke"
"$smoke_dir/libxlsxwriter-smoke" "$smoke_dir/output.xlsx"
test -s "$smoke_dir/output.xlsx"

xlsx_signature=$(od -An -tx1 -N4 "$smoke_dir/output.xlsx" | tr -d '[:space:]')
test "$xlsx_signature" = "504b0304"

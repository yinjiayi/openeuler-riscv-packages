#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libharu libharu-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/pdf.c" <<'EOF'
#include <hpdf.h>
#include <string.h>

int main(int argc, char **argv) {
    HPDF_Doc pdf;
    HPDF_Page page;
    HPDF_Font font;
    HPDF_STATUS result;
    if (argc != 2 || strcmp(HPDF_GetVersion(), "2.4.6") != 0) return 1;
    pdf = HPDF_New(NULL, NULL);
    if (pdf == NULL) return 2;
    page = HPDF_AddPage(pdf);
    if (page == NULL) return 3;
    font = HPDF_GetFont(pdf, "Helvetica", NULL);
    if (font == NULL) return 4;
    result = HPDF_Page_BeginText(page);
    if (result == HPDF_OK) result = HPDF_Page_SetFontAndSize(page, font, 12);
    if (result == HPDF_OK) result = HPDF_Page_TextOut(page, 20, 20, "riscv64 RVA23");
    if (result == HPDF_OK) result = HPDF_Page_EndText(page);
    if (result == HPDF_OK) result = HPDF_SaveToFile(pdf, argv[1]);
    HPDF_Free(pdf);
    return result == HPDF_OK ? 0 : 5;
}
EOF
cc "$smoke_dir/pdf.c" -lhpdf -o "$smoke_dir/pdf"
"$smoke_dir/pdf" "$smoke_dir/output.pdf"
head -c 5 "$smoke_dir/output.pdf" | grep -aFx '%PDF-'
tail -c 16 "$smoke_dir/output.pdf" | grep -aF '%%EOF'
test "$(wc -c < "$smoke_dir/output.pdf")" -gt 200

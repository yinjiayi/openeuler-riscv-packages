#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtiff libtiff-devel libtiff-tools
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <tiffio.h>
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
    TIFF *image;
    uint8_t pixel = 0x5a;
    uint8_t readback = 0;
    uint32_t width = 0;
    if (argc != 2) return 1;
    image = TIFFOpen(argv[1], "w");
    if (image == NULL) return 2;
    TIFFSetField(image, TIFFTAG_IMAGEWIDTH, 1);
    TIFFSetField(image, TIFFTAG_IMAGELENGTH, 1);
    TIFFSetField(image, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(image, TIFFTAG_BITSPERSAMPLE, 8);
    TIFFSetField(image, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);
    TIFFSetField(image, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(image, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_MINISBLACK);
    TIFFSetField(image, TIFFTAG_ROWSPERSTRIP, 1);
    if (TIFFWriteScanline(image, &pixel, 0, 0) != 1) return 3;
    TIFFClose(image);
    image = TIFFOpen(argv[1], "r");
    if (image == NULL) return 4;
    if (!TIFFGetField(image, TIFFTAG_IMAGEWIDTH, &width) || width != 1) return 5;
    if (TIFFReadScanline(image, &readback, 0, 0) != 1 || readback != pixel) return 6;
    TIFFClose(image);
    puts("libtiff-write-read-ok");
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libtiff-4) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/sample.tiff" | grep -Fx 'libtiff-write-read-ok'
tiffinfo "$smoke_dir/sample.tiff" | grep -F 'Image Width: 1 Image Length: 1'

#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libiptcdata libiptcdata-devel
pkg-config --modversion libiptcdata | grep -Fx '1.0.5'
iptc --version | grep -F 'iptc 1.0.5'
rpm -q --provides libiptcdata | grep -F 'libiptcdata.so.0()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat > "$smoke_dir/iptc-smoke.c" <<'EOF'
#include <libiptcdata/iptc-data.h>
#include <string.h>

int main(void) {
    static const unsigned char caption[] = "riscv";
    IptcData *original = iptc_data_new();
    IptcData *parsed;
    IptcDataSet *dataset;
    unsigned char *encoded = 0;
    unsigned int size = 0;
    int ok;
    if (!original) return 1;
    if (iptc_data_add_dataset_with_contents(original, IPTC_RECORD_APP_2,
            IPTC_TAG_CAPTION, caption, sizeof(caption) - 1,
            IPTC_VALIDATE) != (int)(sizeof(caption) - 1)) return 2;
    if (iptc_data_save(original, &encoded, &size) != 0 || !encoded || !size)
        return 3;
    parsed = iptc_data_new_from_data(encoded, size);
    if (!parsed) return 4;
    dataset = iptc_data_get_dataset(parsed, IPTC_RECORD_APP_2,
                                    IPTC_TAG_CAPTION);
    ok = dataset && dataset->size == sizeof(caption) - 1 &&
         memcmp(dataset->data, caption, sizeof(caption) - 1) == 0;
    if (dataset) iptc_dataset_unref(dataset);
    iptc_data_unref(parsed);
    iptc_data_free_buf(original, encoded);
    iptc_data_unref(original);
    return ok ? 0 : 5;
}
EOF
read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libiptcdata)"
cc "$smoke_dir/iptc-smoke.c" "${pkg_flags[@]}" -o "$smoke_dir/iptc-smoke"
"$smoke_dir/iptc-smoke"

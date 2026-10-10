#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libao libao-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <ao/ao.h>

int main(int argc, char **argv) {
    ao_sample_format format = {16, 8000, 1, AO_FMT_NATIVE, NULL};
    char samples[320] = {0};
    ao_device *device;
    int driver;
    if (argc != 2) return 1;
    ao_initialize();
    driver = ao_driver_id("null");
    if (driver < 0) return 2;
    device = ao_open_live(driver, &format, NULL);
    if (device == NULL || !ao_play(device, samples, sizeof(samples)) || !ao_close(device)) return 3;
    driver = ao_driver_id("wav");
    if (driver < 0) return 4;
    device = ao_open_file(driver, argv[1], 1, &format, NULL);
    if (device == NULL || !ao_play(device, samples, sizeof(samples)) || !ao_close(device)) return 5;
    ao_shutdown();
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs ao) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/output.wav"
test -s "$smoke_dir/output.wav"
test "$(head -c 4 "$smoke_dir/output.wav")" = RIFF
test -f /usr/lib64/ao/plugins-4/libalsa.so
test -f /usr/lib64/ao/plugins-4/libpulse.so

#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- opus opus-devel opus-help
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <opus/opus.h>

int main(void) {
    OpusEncoder *encoder;
    OpusDecoder *decoder;
    opus_int16 input[960] = {0};
    opus_int16 output[960];
    unsigned char packet[4000];
    int error;
    int packet_size;
    int decoded_samples;

    encoder = opus_encoder_create(48000, 1, OPUS_APPLICATION_AUDIO, &error);
    if (encoder == NULL || error != OPUS_OK) return 1;
    decoder = opus_decoder_create(48000, 1, &error);
    if (decoder == NULL || error != OPUS_OK) return 2;

    packet_size = opus_encode(encoder, input, 960, packet, sizeof(packet));
    if (packet_size <= 0) return 3;
    decoded_samples = opus_decode(decoder, packet, packet_size, output, 960, 0);
    opus_encoder_destroy(encoder);
    opus_decoder_destroy(decoder);
    return decoded_samples == 960 ? 0 : 4;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs opus) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- wget2 wget2-libs wget2-devel
rpm -V -- wget2 wget2-libs wget2-devel
wget2 --version | grep -F -- 'GNU Wget2 2.2.1' >/dev/null

for package in wget2 wget2-libs wget2-devel; do
    mapfile -t paths < <(rpm -ql -- "$package")
    for record in \
      'COPYING:e79e9c8a0c85d735ff98185918ec94ed7d175efc377012787aebcf3b80f0d90b' \
      'COPYING.LESSER:e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118' \
      'COPYING.GFDL13:110535522396708cea37c72a802c5e7e81391139f5f7985631c93ef242b206a4'; do
        name=${record%%:*}
        digest=${record#*:}
        found=0
        for path in "${paths[@]}"; do
            if [[ "$path" == /usr/share/licenses/*/"$name" ]]; then
                printf '%s  %s\n' "$digest" "$path" | sha256sum -c -
                found=$((found + 1))
            fi
        done
        test "$found" -eq 1
    done
done

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <wget.h>

int main(void) {
    wget_global_init(0);
    wget_global_deinit();
    return 0;
}
EOF

cc $(pkg-config --cflags libwget) "$smoke_dir/smoke.c" \
  $(pkg-config --libs libwget) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

# Explicitly downstream semantic transfer; all traffic stays on loopback.
python3 - "$smoke_dir" <<'PY'
import http.server
import pathlib
import subprocess
import sys
import threading

payload = b"wget2 downstream loopback fixture\n\x00\xff\n"
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/fixture":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
output = pathlib.Path(sys.argv[1]) / "download"
try:
    subprocess.run(["wget2", "--no-proxy", "--no-config", "--timeout=10", "--tries=1",
                    "--output-document=" + str(output),
                    "http://127.0.0.1:%d/fixture" % server.server_port],
                   check=True, timeout=20)
    assert output.read_bytes() == payload, "installed HTTP payload mismatch"
finally:
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()
assert not thread.is_alive()
print("PASS downstream installed loopback HTTP exact payload; no upstream suite count")
PY

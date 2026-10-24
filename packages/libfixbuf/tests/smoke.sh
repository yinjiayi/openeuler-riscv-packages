#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -f /usr/lib64/libfixbuf.so.9.1.2
test -f /usr/lib64/libfixbuf.a
test -f /usr/include/fixbuf/public.h
test -f /usr/lib64/pkgconfig/libfixbuf.pc
cd /usr/share/licenses/libfixbuf/license-notices
sha256sum -c SHA256SUMS
cd /usr/libexec/libfixbuf-tests
sha256sum -c SHA256SUMS
trace="$(mktemp)"
trap 'rm -f "$trace"' EXIT
if LD_DEBUG=bindings ./api-smoke 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libfixbuf installed raw loader trace'
cat "$trace"
echo 'END libfixbuf installed raw loader trace'
sha256sum "$trace"
test "$(readlink -f /lib64/libfixbuf.so.9)" = /usr/lib64/libfixbuf.so.9.1.2
test "$(readlink -f /usr/lib64/libfixbuf.so.9)" = /usr/lib64/libfixbuf.so.9.1.2
for symbol in fbInfoModelAlloc fbTemplateAppendSpecArray fBufAppend fBufNext; do
    grep -E "binding file .*api-smoke.* to (/usr)?/lib64/libfixbuf\.so\.9([ .]|$).*symbol .${symbol}[^[:alnum:]_]" "$trace"
done
echo 'libfixbuf installed API replay and four library bindings PASS'

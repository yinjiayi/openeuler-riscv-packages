#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bmake mk-files
test "$(bmake -r -f /dev/null -V .MAKE.VERSION)" = "20260714"
test "$(bmake -r -f /dev/null -V .MAKE.OS)" = "Linux"
test "$(bmake -f /dev/null -V .SYSPATH)" = "/usr/share/mk"
test -r /usr/share/mk/sys.mk
test -L /usr/share/mk/bsd.prog.mk
test "$(readlink /usr/share/mk/bsd.prog.mk)" = "prog.mk"
test "$(head -n 1 /usr/share/mk/meta2deps.py)" = "#!/usr/bin/python3"

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/Makefile" <<'EOF'
MESSAGE = openEuler-RVA23

all: result.txt

result.txt:
	@printf '%s\n' '${MESSAGE}' > ${.TARGET}
EOF

bmake -C "$smoke_dir"
test "$(cat "$smoke_dir/result.txt")" = "openEuler-RVA23"
bmake -C "$smoke_dir" -V MESSAGE | grep -Fx 'openEuler-RVA23'

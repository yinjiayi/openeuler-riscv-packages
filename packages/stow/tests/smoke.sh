#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- stow
/usr/bin/stow --version | grep -F 'stow (GNU Stow) version 2.4.1'
perl -MStow -e 'die "wrong Stow version\n" unless $Stow::VERSION eq "2.4.1"'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
mkdir -p "$smoke_dir/packages/example/bin" "$smoke_dir/target"
printf '#!/usr/bin/env sh\nprintf "stow-rva23-smoke\\n"\n' \
  >"$smoke_dir/packages/example/bin/stow-rva23-smoke"
chmod 0755 "$smoke_dir/packages/example/bin/stow-rva23-smoke"

/usr/bin/stow --dir="$smoke_dir/packages" --target="$smoke_dir/target" example
test -L "$smoke_dir/target/bin"
test "$(readlink "$smoke_dir/target/bin")" = '../packages/example/bin'
test "$("$smoke_dir/target/bin/stow-rva23-smoke")" = 'stow-rva23-smoke'
/usr/bin/stow --delete --dir="$smoke_dir/packages" \
  --target="$smoke_dir/target" example
test ! -e "$smoke_dir/target/bin"

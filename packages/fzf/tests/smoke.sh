#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- fzf
fzf --version | grep -F '0.74.3 (source)'
result=$(printf 'alpha\nbeta\ngamma\n' | fzf --filter=alp --no-sort)
test "$result" = alpha
test -x /usr/bin/fzf-tmux
test -r /usr/share/man/man1/fzf.1.gz
test -r /usr/share/bash-completion/completions/fzf
test -r /usr/share/zsh/site-functions/_fzf

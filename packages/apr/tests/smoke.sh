#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- apr apr-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <apr_general.h>
#include <apr_pools.h>
int main(void){apr_pool_t *p=0;if(apr_initialize()!=APR_SUCCESS)return 1;if(apr_pool_create(&p,0)!=APR_SUCCESS)return 2;apr_pool_destroy(p);apr_terminate();return 0;}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(apr-1-config --includes --link-ld --libs)
"$d/smoke"

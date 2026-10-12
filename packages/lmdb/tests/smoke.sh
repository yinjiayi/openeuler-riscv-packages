#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- lmdb lmdb-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <lmdb.h>

int main(int argc, char **argv)
{
    MDB_env *env;
    MDB_txn *txn;
    MDB_dbi dbi;
    MDB_val key = {3, "key"};
    MDB_val value = {5, "RVA23"};

    if (argc != 2 || mdb_env_create(&env) != 0)
        return 1;
    if (mdb_env_open(env, argv[1], 0, 0600) != 0)
        return 2;
    if (mdb_txn_begin(env, NULL, 0, &txn) != 0)
        return 3;
    if (mdb_dbi_open(txn, NULL, 0, &dbi) != 0)
        return 4;
    if (mdb_put(txn, dbi, &key, &value, 0) != 0)
        return 5;
    if (mdb_txn_commit(txn) != 0)
        return 6;
    mdb_env_close(env);
    return 0;
}
EOF
mkdir "$d/db"
gcc "$d/smoke.c" -o "$d/smoke" -llmdb
"$d/smoke" "$d/db"
mdb_stat -e "$d/db" >/dev/null

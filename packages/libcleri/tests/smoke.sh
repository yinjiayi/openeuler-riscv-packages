#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcleri libcleri-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <cleri/cleri.h>
#include <string.h>

static int parse_matches(cleri_grammar_t *grammar, const char *input, int expected) {
    cleri_parse_t *result = cleri_parse(grammar, input);
    if (result == NULL) return 0;
    int matched = result->is_valid == expected;
    cleri_parse_free(result);
    return matched;
}

int main(void) {
    cleri_t *keyword;
    cleri_t *name;
    cleri_t *sequence;
    cleri_grammar_t *grammar;
    int ok;
    if (strcmp(cleri_version(), "1.0.2") != 0) return 1;
    keyword = cleri_keyword(0, "hi", 0);
    name = cleri_regex(0, "^(?:\"(?:[^\"]*)\")+");
    sequence = cleri_sequence(0, 2, keyword, name);
    grammar = cleri_grammar(sequence, NULL);
    if (grammar == NULL) return 2;
    ok = parse_matches(grammar, "hi \"Iris\"", 1) &&
         parse_matches(grammar, "bye \"Iris\"", 0);
    cleri_grammar_free(grammar);
    return ok ? 0 : 3;
}
EOF

cc "$smoke_dir/smoke.c" -lcleri -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

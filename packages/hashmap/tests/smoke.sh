#!/bin/bash
set -euo pipefail
test -f /usr/include/hashmap.h
test -f /usr/lib64/libhashmap.a
rpm -V hashmap hashmap-tests
run_installed_defaults() {
    root=$1
    qa="$root/usr/share/hashmap/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=c99 -DHASHMAP_TEST "$qa/hashmap.c" -o "$temp/original-test"
    env -u BENCH -u N -u SEED "$temp/original-test" > "$temp/original.log"
    cat "$temp/original.log"
    grep -qx 'PASSED' "$temp/original.log"
    gcc -O2 -g -UNDEBUG -std=c99 -I"$root/usr/include" -x c - -x none "$root/usr/lib64/libhashmap.a" -o "$temp/consumer" <<'C'
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <hashmap.h>
static uint64_t hash(const void *p,uint64_t a,uint64_t b) { return hashmap_sip(p,sizeof(int),a,b); }
static int compare(const void *a,const void *b,void *u) { (void)u; return (*(const int*)a>*(const int*)b)-(*(const int*)a<*(const int*)b); }
int main(void) {
    struct hashmap *m=hashmap_new(sizeof(int),0,1,2,hash,compare,0,0);
    assert(m && hashmap_count(m)==0);
    for(int i=0;i<2000;i++) { assert(!hashmap_set(m,&i)); assert(!hashmap_oom(m)); }
    assert(hashmap_count(m)==2000);
    for(int i=0;i<2000;i++) { const int *p=hashmap_get(m,&i); assert(p && *p==i); }
    size_t iter=0,n=0;void *item;
    while(hashmap_iter(m,&iter,&item)) { assert(item); n++; }
    assert(n==2000);
    for(int i=0;i<2000;i++) { const int *p=hashmap_delete(m,&i); assert(p && *p==i); }
    assert(hashmap_count(m)==0);hashmap_free(m);
    assert(hashmap_sip("hello",5,1,2)==2957200328589801622ULL);
    assert(hashmap_murmur("hello",5,1,2)==1682575153221130884ULL);
    assert(hashmap_xxhash3("hello",5,1,2)==2584346877953614258ULL);
    return 0;
}
C
    "$temp/consumer"
    rm -f "$temp/original-test" "$temp/original.log" "$temp/consumer"
    rmdir "$temp"
    echo 'PASS hashmap original-defaults=2000 installed-archive=2000 skips=0'
}
run_installed_defaults ''

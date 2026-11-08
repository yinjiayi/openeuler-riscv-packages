#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libgeome/qa/libgeome-1.0.tar.gz"
    echo '28f17577d0b264bec90cf0adb2ee23a51178a227138a6026f1b46cfd028a32a6  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT HUP INT TERM
    tar -xzf "$archive" -C "$work"
    original="$work/libgeome"
    libdir="$root/usr/lib64"
    export LD_LIBRARY_PATH="$libdir"
    export TZ=Etc/UTC
    export TZDIR="$work/zoneinfo"
    mkdir -p "$TZDIR" "$work/bin"
    printf 'ZZ\t+0000+00000\tEtc/UTC\n' > "$TZDIR/zone1970.tab"
    printf '12.5 -45.25\n' > "$work/location"
    # Original netservice driver and all seven service entries remain unchanged.
    # A deterministic executable replaces only the third-party HTTP transport.
    printf '#!/bin/sh\nprintf "12.5 -45.25\\n"\n' > "$work/bin/curl"
    chmod 0755 "$work/bin/curl"
    export PATH="$work/bin:$PATH"
    for linkage in static shared; do
        if test "$linkage" = static; then set -- "$libdir/libgeome.a"; else set -- -L"$libdir" -lgeome; fi
        for driver in time timezone file command netservice; do
            gcc -std=c99 -D_DEFAULT_SOURCE -I"$root/usr/include" -I"$original" -Wall -Wextra -o "$work/$driver-$linkage" "$original/test-$driver.c" "$original/test-common.c" "$@" -lm
        done
        "$work/time-$linkage" > "$work/out"
        grep -Fx 'Longitude: 0' "$work/out"
        "$work/timezone-$linkage" > "$work/out"
        grep -Fx 'Latitude:  0' "$work/out"
        grep -Fx 'Longitude: 0' "$work/out"
        "$work/file-$linkage" "$work/location" > "$work/out"
        grep -Fx 'Latitude:  12.5' "$work/out"
        grep -Fx 'Longitude: -45.25' "$work/out"
        "$work/command-$linkage" sh -c 'printf "12.5 -45.25\n"' > "$work/out"
        grep -Fx 'Latitude:  12.5' "$work/out"
        "$work/netservice-$linkage" > "$work/out"
        test "$(grep -c '^Latitude:  12.5$' "$work/out")" -eq 7
    done
    cat > "$work/consumer.c" <<'C'
#define _GNU_SOURCE
#include <libgeome.h>
#include <assert.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static struct libgeome_context ctx;
static struct libgeome_data out;
static void reset(void) { memset(&out,0,sizeof(out)); out.requested_data=7; }
static int command(const char *text,size_t limit) {
    const char *args[]={"printf","%s",text,NULL}; reset();
    return libgeome_get_from_command(&ctx,&out,limit,5,"printf",args);
}
static size_t descriptors(void) { DIR *d=opendir("/proc/self/fd"); struct dirent *p; size_t n=0; assert(d); while((p=readdir(d))) n++; closedir(d); return n; }
int main(int argc,char **argv) {
    const char *good[]={"12.5 -45.25","12.5,-45.25","{\"lat\":12.5,\"lon\":-45.25}","<lat>12.5</lat><lon>-45.25</lon>"};
    const char *bad[]={" ",",","12.5 ","{\"lat\":,\"lon\":}","<lat></lat><lon></lon>","\xff"};
    size_t i,n; FILE *f; assert(argc==2); libgeome_basic_context(&ctx,"installed-geome");
    for(i=0;i<sizeof(good)/sizeof(*good);i++) { assert(!command(good[i],0)); assert(out.requested_data==3); assert(fabs(out.latitude-12.5)<1e-9 && fabs(out.longitude+45.25)<1e-9); }
    for(i=0;i<sizeof(bad)/sizeof(*bad);i++) { assert(!command(bad[i],0)); assert(!out.requested_data); }
    assert(!command("90 180",6) && out.requested_data==3);
    assert(command("90 180x",6));
    assert(!command("91 181",0) && !out.requested_data);
    n=descriptors(); for(i=0;i<64;i++) assert(!command("12.5 -45.25",0)); assert(descriptors()==n);
    f=fopen(argv[1],"w"); assert(f); fputs(" \n",f); assert(!fclose(f)); reset(); assert(libgeome_get_from_file(&ctx,&out,argv[1]));
    f=fopen(argv[1],"w"); assert(f); fputs("12.5:-45.25\n",f); assert(!fclose(f)); reset(); assert(!libgeome_get_from_file(&ctx,&out,argv[1]) && out.requested_data==3);
    assert(libgeome_netservices_count==7);
    puts("PASS geome installed input formats, invalid/empty/range/limit and pipe-lifetime regressions");
    return 0;
}
C
    for linkage in static shared; do
        if test "$linkage" = static; then set -- "$libdir/libgeome.a"; else set -- -L"$libdir" -lgeome; fi
        gcc -std=c99 -I"$root/usr/include" -Wall -Wextra -Werror -o "$work/consumer-$linkage" "$work/consumer.c" "$@" -lm
        "$work/consumer-$linkage" "$work/location"
    done
    # Malformed timezone table must fail without indexing beyond the field.
    printf 'ZZ\t+0\tEtc/UTC\n' > "$TZDIR/zone1970.tab"
    if "$work/timezone-shared"; then exit 1; fi
    echo 'PASS geome all five original drivers with offline transport fixtures and static/shared installed regressions'
)
run_installed_tests ''

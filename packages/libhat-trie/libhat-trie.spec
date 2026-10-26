# SPDX-License-Identifier: Apache-2.0
# Upstream installs a static archive and no ELF payload. Avoid an empty automatic
# debuginfo subpackage; preserve compiler flags, archive processing and all QA.
%global debug_package %{nil}
Name:           libhat-trie
Version:        0.1.2
Release:        2%{?dist}
Summary:        Cache-conscious string trie and array hash table library
License:        LicenseRef-hat-trie-MIT-truncated AND BSD-3-Clause AND LGPL-2.1-only AND LicenseRef-Public-Domain AND ISC AND Apache-2.0
URL:            https://github.com/dcjones/hat-trie
Source0:        hat-trie-0.1.2.tar.gz
Source1:        LGPL-2.1.txt
Source2:        Apache-2.0.txt
Patch0:         0001-preserve-flags-fix-pc-and-clear-counts.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gcc
Requires:       glibc-devel
Requires:       grep
Requires:       pkgconf-pkg-config

%description
A cache-conscious HAT-trie and array hash table implementation. This package
keeps upstream's default static library, five public headers and pkg-config
metadata. Its installed test source consumes the installed static archive.

%prep
%setup -q -n dcjones-hat-trie-6dfc9ed
# Snapshot all 27 original members before any patch, generated helper or QA file.
find . -type f -print | LC_ALL=C sort > ../hat-trie-original-members.list
test "$(wc -l < ../hat-trie-original-members.list)" -eq 27
mkdir license-notices
while IFS= read -r item; do
    rel="${item#./}"
    mkdir -p "license-notices/$(dirname "$rel")"
    cp -p "$item" "license-notices/$rel.notice"
done < ../hat-trie-original-members.list
(cd license-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../hat-trie-original-SHA256SUMS
mv ../hat-trie-original-SHA256SUMS license-notices/SHA256SUMS
test "$(wc -l < license-notices/SHA256SUMS)" -eq 27
cp -p %{SOURCE1} LGPL-2.1.txt
cp -p %{SOURCE2} Apache-2.0.txt
cat > SuperFastHash-attribution.notice <<'NOTICE'
The SuperFastHash-derived hash in original test/str_map.c is by Paul Hsieh.
Original source attribution: http://www.azillionmonkeys.com/qed/hash.html
Official author page captured 2026-10-26:
https://www.azillionmonkeys.com/qed/hash.html
The author additionally offers the code displayed on that page under LGPL 2.1,
limited to that code, not all other archives or listings. This package elects
LGPL-2.1-only for the derivative hash in test/str_map.c, not multiple licenses.
The retained fork renames SuperFastHash to hash, changes length int to size_t,
and removes the signed-char casts in the three-byte and one-byte tail cases.
It is modified code, not a claim of byte identity or historical grant date.
The full LGPL-2.1 text is installed as LGPL-2.1.txt. Original Daniel C. Jones
copyright/project grant and every original source member remain byte-preserved
in license-notices. The distinct BSD-3-Clause grant in src/pstdint.h applies to
that header; it is not borrowed to license this hash. Public-domain declarations
in src/portable_endian.h and original MurmurHash3 are preserved separately.
COPYING is retained verbatim, including its originally truncated disclaimer.
NOTICE
%autopatch -p1
cat > api-smoke.c <<'C'
/* ISC License
 * Copyright (c) 2026 openEuler RISC-V package contributors
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <hat-trie.h>
#include <ahtable.h>
#include <common.h>
#include <pstdint.h>
#include <portable_endian.h>
static value_t *(*volatile get)(hattrie_t *, const char *, size_t) = hattrie_get;
static value_t *(*volatile lookup)(hattrie_t *, const char *, size_t) = hattrie_tryget;
static void (*volatile clear_trie)(hattrie_t *) = hattrie_clear;
static void (*volatile clear_table)(ahtable_t *) = ahtable_clear;
static void (*volatile save_table)(const ahtable_t *, FILE *) = ahtable_save;
static ahtable_t *(*volatile load_table)(FILE *) = ahtable_load;
static const unsigned char keys[4][3] = {{'a',0,0},{'a',0,'b'},{'a',0,'c'},{0x81,0x70,0}};
static const size_t lens[4] = {1,3,3,2};
static int key_index(const char *key, size_t len) {
    for (int i=0;i<4;i++) if (len==lens[i] && !memcmp(key,keys[i],len)) return i;
    return -1;
}
static hattrie_t *binary_trie(void) {
    hattrie_t *t=hattrie_create(); assert(t);
    for (int i=0;i<4;i++) *get(t,(const char *)keys[i],lens[i])=(value_t)(i+11);
    return t;
}
int main(void) {
    hattrie_t *t=hattrie_create(); assert(t && hattrie_size(t)==0);
    assert(!lookup(t,"missing",7) && hattrie_size(t)==0);
    value_t *v=get(t,"alpha",5); assert(v && *v==0); *v=31;
    assert(hattrie_size(t)==1 && *lookup(t,"alpha",5)==31);
    *get(t,"alpha",5)=47; assert(hattrie_size(t)==1 && *lookup(t,"alpha",5)==47);
    hattrie_free(t); puts("case 1 create missing insert overwrite PASS");
    t=binary_trie(); assert(hattrie_size(t)==4);
    for (int i=0;i<4;i++) assert(*lookup(t,(const char *)keys[i],lens[i])==(value_t)(i+11));
    assert(!lookup(t,"a\0d",3)); hattrie_free(t);
    puts("case 2 nonempty binary key isolation PASS");
    t=binary_trie();
    for (int sorted=0;sorted<2;sorted++) {
        unsigned seen=0; size_t count=0, prevlen=0; unsigned char prev[8]={0};
        hattrie_iter_t *it=hattrie_iter_begin(t,sorted!=0); assert(it);
        while (!hattrie_iter_finished(it)) {
            size_t len=0; const char *key=hattrie_iter_key(it,&len);
            assert(key && len<=sizeof(prev)); int i=key_index(key,len); assert(i>=0);
            assert(!(seen&(1u<<i)) && *hattrie_iter_val(it)==(value_t)(i+11));
            if (sorted && count) { size_t n=prevlen<len?prevlen:len; int c=memcmp(prev,key,n); assert(c<0 || (c==0 && prevlen<len)); }
            memcpy(prev,key,len); prevlen=len; seen|=1u<<i; count++; hattrie_iter_next(it);
        }
        assert(count==4 && seen==15);
        size_t endlen=123; assert(hattrie_iter_key(it,&endlen)==NULL && hattrie_iter_val(it)==NULL);
        hattrie_iter_free(it);
    }
    hattrie_free(t); puts("case 3 sorted unsorted exact iteration PASS");
    t=binary_trie(); int payload=99;
    *get(t,"payload",7)=(value_t)(uintptr_t)&payload;
    assert((int *)(uintptr_t)*lookup(t,"payload",7)==&payload);
    assert(hattrie_del(t,(const char *)keys[1],lens[1])==0 && hattrie_size(t)==4);
    assert(!lookup(t,(const char *)keys[1],lens[1]));
    assert(hattrie_del(t,(const char *)keys[1],lens[1])==-1 && hattrie_size(t)==4);
    assert(*lookup(t,(const char *)keys[2],lens[2])==13);
    hattrie_free(t); puts("case 4 delete status cardinality payload PASS");
    t=binary_trie(); clear_trie(t); assert(hattrie_size(t)==0 && !lookup(t,"a",1));
    hattrie_iter_t *empty=hattrie_iter_begin(t,false); assert(hattrie_iter_finished(empty)); hattrie_iter_free(empty);
    *get(t,"again",5)=73; assert(hattrie_size(t)==1 && *lookup(t,"again",5)==73);
    clear_trie(t); assert(hattrie_size(t)==0 && !lookup(t,"again",5)); hattrie_free(t);
    puts("case 5 populated trie clear reinsert repeat PASS");
    ahtable_t *a=ahtable_create_n(1); assert(a);
    *ahtable_get(a,"a\0b",3)=123; *ahtable_get(a,"plain",5)=456;
    assert(ahtable_size(a)==2);
    FILE *f=tmpfile(); assert(f); save_table(a,f); assert(fflush(f)==0 && fseek(f,0,SEEK_SET)==0);
    ahtable_t *b=load_table(f); assert(b && ahtable_size(b)==2);
    assert(*ahtable_tryget(b,"a\0b",3)==123 && *ahtable_tryget(b,"plain",5)==456);
    assert(fclose(f)==0); ahtable_free(b);
    clear_table(a); assert(ahtable_size(a)==0 && !ahtable_tryget(a,"plain",5));
    assert(a->n==ahtable_initial_size && a->max_m==(size_t)(ahtable_max_load_factor*(double)a->n));
    *ahtable_get(a,"again",5)=19; assert(ahtable_size(a)==1); clear_table(a); assert(ahtable_size(a)==0);
    ahtable_free(a); puts("case 6 array table file roundtrip clear counts PASS");
    puts("libhat-trie six strict static API cases PASS"); return 0;
}
C
cat > expected.stdout <<'EXPECTED'
case 1 create missing insert overwrite PASS
case 2 nonempty binary key isolation PASS
case 3 sorted unsorted exact iteration PASS
case 4 delete status cardinality payload PASS
case 5 populated trie clear reinsert repeat PASS
case 6 array table file roundtrip clear counts PASS
libhat-trie six strict static API cases PASS
EXPECTED

%build
autoreconf -fi
# Preserve feature defaults: AC_DISABLE_SHARED; no synthetic shared variant.
./configure --prefix=%{_prefix} --libdir=%{_libdir} --includedir=%{_includedir} CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
%make_build
gcc %{optflags} -UNDEBUG -Isrc api-smoke.c src/.libs/libhat-trie.a %{build_ldflags} -o api-smoke

%install
%make_install
install -Dpm 0644 api-smoke.c %{buildroot}%{_datadir}/%{name}-tests/api-smoke.c
install -Dpm 0644 expected.stdout %{buildroot}%{_datadir}/%{name}-tests/expected.stdout

%check
(cd license-notices; sha256sum -c SHA256SUMS)
if %make_build check > original-make-check.log 2>&1; then cat original-make-check.log; else status=$?; cat original-make-check.log; exit "$status"; fi
test -x test/check_ahtable && test -x test/check_hattrie && test -x test/bench_sorted_iter
grep -Fx ':test-result: PASS' test/check_ahtable.trs
grep -Fx ':test-result: PASS' test/check_hattrie.trs
if grep -F -e '[error]' -e "can't store non-ascii strings" original-make-check.log test/check_ahtable.log test/check_hattrie.log; then exit 1; fi
if ./api-smoke > api.stdout 2> api.stderr; then :; else status=$?; cat api.stdout api.stderr; exit "$status"; fi
cat api.stdout
cmp expected.stdout api.stdout
test ! -s api.stderr
# %check follows RPM install-post: capture final installed archive/header bytes.
cd %{buildroot}
sha256sum usr/lib64/libhat-trie.a usr/lib64/libhat-trie.la usr/lib64/pkgconfig/hat-trie-0.1.pc usr/include/hat-trie/hat-trie.h usr/include/hat-trie/ahtable.h usr/include/hat-trie/common.h usr/include/hat-trie/pstdint.h usr/include/hat-trie/portable_endian.h usr/share/libhat-trie-tests/api-smoke.c usr/share/libhat-trie-tests/expected.stdout > usr/share/libhat-trie-tests/SHA256SUMS

%files
%license COPYING LGPL-2.1.txt Apache-2.0.txt SuperFastHash-attribution.notice license-notices
%doc README.md
%{_libdir}/libhat-trie.a
%{_libdir}/libhat-trie.la
%{_libdir}/pkgconfig/hat-trie-0.1.pc
%dir %{_includedir}/hat-trie
%{_includedir}/hat-trie/hat-trie.h
%{_includedir}/hat-trie/ahtable.h
%{_includedir}/hat-trie/common.h
%{_includedir}/hat-trie/pstdint.h
%{_includedir}/hat-trie/portable_endian.h
%{_datadir}/%{name}-tests

%changelog
* Mon Oct 26 2026 openEuler RISC-V package contributors - 0.1.2-2
- Avoid the empty automatic debuginfo subpackage for the static-only payload.

* Mon Oct 26 2026 openEuler RISC-V package contributors - 0.1.2-1
- Preserve upstream static/default checks with explicit rights and strict API QA.

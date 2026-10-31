# SPDX-License-Identifier: MIT AND BSD-2-Clause AND CC0-1.0
%global debug_package %{nil}
%global upstream_commit 3735986914fc1c4e6a9123b406d0970666aa4aec

Name:           hashmap
Version:        0.9.0
Release:        1
Summary:        Generic Robin Hood hash map implementation for C
License:        MIT AND BSD-2-Clause AND CC0-1.0
URL:            https://github.com/tidwall/hashmap.c
Source0:        https://codeload.github.com/tidwall/hashmap.c/tar.gz/%{upstream_commit}#/hashmap-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/spdx/license-list-data/d46e94e2c78ceede1cfc63cfa0396472d2798d4c/text/CC0-1.0.txt
Source2:        https://raw.githubusercontent.com/spdx/license-list-data/d46e94e2c78ceede1cfc63cfa0396472d2798d4c/text/BSD-2-Clause.txt
BuildRequires:  gcc
BuildRequires:  binutils
BuildRequires:  bash
BuildRequires:  coreutils

%description
Generic C99 Robin Hood hash map with custom allocators and SipHash, MurmurHash3
and xxHash helpers. This package installs the public header and static archive.

%package tests
Summary:        Original default hash map tests and installed archive consumer
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       binutils
Requires:       bash
Requires:       coreutils

%description tests
Unchanged upstream test source and a downstream installed-library consumer.
The original suite uses all 2000 default elements and allocation-failure tests.

%prep
%setup -q -n hashmap.c-%{upstream_commit}
cp -p %{SOURCE1} CC0-1.0.txt
sed 's/<year> <owner>/2012-2021 Yann Collet/' %{SOURCE2} > BSD-2-Clause.txt

%build
gcc %{optflags} -UNDEBUG -std=c99 -c hashmap.c -o hashmap.o
ar rcs libhashmap.a hashmap.o
gcc %{optflags} -UNDEBUG -std=c99 -DHASHMAP_TEST hashmap.c -o upstream-test

%install
install -Dpm0644 hashmap.h %{buildroot}%{_includedir}/hashmap.h
install -Dpm0644 libhashmap.a %{buildroot}%{_libdir}/libhashmap.a
install -Dpm0644 hashmap.c %{buildroot}%{_datadir}/hashmap/qa/hashmap.c
install -Dpm0644 hashmap.h %{buildroot}%{_datadir}/hashmap/qa/hashmap.h

%check
env -u BENCH -u N -u SEED ./upstream-test > default-test.log
cat default-test.log
grep -qx 'PASSED' default-test.log
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
run_installed_defaults '%{buildroot}'

%files
%license LICENSE CC0-1.0.txt BSD-2-Clause.txt
%doc README.md
%{_includedir}/hashmap.h
%{_libdir}/libhashmap.a

%files tests
%license LICENSE CC0-1.0.txt BSD-2-Clause.txt
%{_datadir}/hashmap

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.9.0-1
- Preserve original default tests, source notices and complete embedded licenses.

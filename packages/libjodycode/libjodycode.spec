# SPDX-License-Identifier: Apache-2.0
Name:           libjodycode
Version:        4.2
Release:        1%{?dist}
Summary:        Portable C helper library and noncryptographic hash functions
License:        MIT AND LicenseRef-Public-Domain AND Apache-2.0
URL:            https://codeberg.org/jbruchon/libjodycode
Source0:        libjodycode-4.2.tar.gz
Source1:        Apache-2.0.txt
Patch0:         0001-initialize-relative-result-and-continue-casefold.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gawk
Requires:       gcc
Requires:       glibc-devel
Requires:       grep

%description
Portable C helpers, file and string wrappers, version interfaces and the
noncryptographic jody hash. Original shared/static libraries, public header
and manual are retained. The official release tag is v4.2; this exact source
declares header/library version 4.2.0, API 4, feature level 6.

%prep
%setup -q -n libjodycode
find . -type f -print | LC_ALL=C sort > ../libjodycode-original-members.list
test "$(wc -l < ../libjodycode-original-members.list)" -eq 81
mkdir license-notices
while IFS= read -r item; do
    rel="${item#./}"
    mkdir -p "license-notices/$(dirname "$rel")"
    cp -p "$item" "license-notices/$rel.notice"
    chmod 0644 "license-notices/$rel.notice"
done < ../libjodycode-original-members.list
(cd license-notices; find . -type f -name '*.notice' -print | LC_ALL=C sort | while IFS= read -r item; do sha256sum "$item"; done) > ../libjodycode-original-SHA256SUMS
mv ../libjodycode-original-SHA256SUMS license-notices/SHA256SUMS
test "$(wc -l < license-notices/SHA256SUMS)" -eq 81
cp -p %{SOURCE1} Apache-2.0.txt
cat > Public-Domain.notice <<'NOTICE'
LicenseRef-Public-Domain identifies the original explicit public-domain
declarations by Jody Bruchon, retained verbatim in these complete notices:
  c99_aligned_alloc.c.notice
  c99_aligned_alloc.h.notice
  likely_unlikely.h.notice
  helper_code/libjodycode_apiver.c.notice
The c99_aligned_alloc pair additionally offers CC0; this package selects the
expressly stated public-domain branch and does not claim a fetched CC0 text.
All remaining source is retained under the complete project MIT grant and
original per-file notices. The unmodified skeleton's MIT grant includes an
optional permission to relicense modified projects, not exercised here.
These statements describe author declarations, not universal legal advice.
NOTICE
%autopatch -p1
cat > api-smoke.c <<'C'
/* Copyright 2026 openEuler RISC-V package contributors
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * https://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. Full text is shipped as Apache-2.0.txt.
 * Hash reference recurrence follows Jody Bruchon's MIT-licensed jody_hash.c;
 * the original full source/copyright/grant remain in license-notices/LICENSE.txt.notice.
 * It is a bounded consistency oracle, not independent cryptanalysis.
 */
#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libjodycode.h>
static int (*volatile hash_fn)(enum jc_e_hash,jodyhash_t *,jodyhash_t *,size_t)=jc_block_hash;
static int (*volatile numeric_fn)(const char *,const char *,int)=jc_numeric_strcmp;
static JC_STR_T *(*volatile string_fn)(const char *,uint32_t)=jc_str_init;
static int (*volatile relative_fn)(const char *,const char *,char *)=jc_make_relative_link_name;
static size_t (*volatile read_fn)(void *,size_t,size_t,FILE *)=jc_fread;
static long (*volatile strtol_fn)(const char *,char **,int)=jc_strtol;
static uint64_t rol(uint64_t x,unsigned n) { return (x<<n)|(x>>(64-n)); }
static uint64_t ror(uint64_t x,unsigned n) { return (x>>n)|(x<<(64-n)); }
static uint64_t reference(const uint64_t *data,size_t bytes,uint64_t h) {
    const uint64_t c=UINT64_C(0x71812e0f5463d3c8);
    size_t words=bytes/8;
    for (size_t i=0;i<words;i++) { uint64_t a=data[i]+c,b=ror(data[i],14)^ror(c,28); h+=a; h^=b; h=rol(h,28); h+=a; }
    unsigned tail=(unsigned)(bytes&7);
    if (tail) { uint64_t x=data[words]&((UINT64_C(1)<<(tail*8))-1),a=x+c,b=ror(x,14)^ror(c,28); h+=a; h^=b; h=rol(h,28); h+=b; }
    return h;
}
int main(void) {
    assert(!strcmp(jc_version,"4.2.0") && !strcmp(jc_verdate,"2026-10-20"));
    assert(jc_api_version==4 && jc_api_featurelevel==6 && jc_jodyhash_version==7 && jc_windows_unicode==0);
    assert(!strcmp(LIBJODYCODE_VER,"4.2.0") && LIBJODYCODE_API_FEATURE_LEVEL==6);
    char *end=NULL; jc_errno=0;
    assert(strtol_fn("123tail",&end,10)==123 && !strcmp(end,"tail") && jc_errno==0);
    jc_errno=0; assert(strtol_fn("99999999999999999999999999999999999",&end,10)==LONG_MAX && jc_errno==ERANGE);
    jc_errno=0; assert(strtol_fn(NULL,&end,10)==0 && jc_errno==EFAULT);
    assert(!strcmp(jc_get_errname(JC_ENULL),"null"));
    puts("case 1 actual ABI version numeric errors PASS");
    uint64_t data[1025]; for (size_t i=0;i<1025;i++) data[i]=(uint64_t)i*UINT64_C(0x102030405060708)^UINT64_C(0xabcdef0123456789);
    uint64_t h=0; assert(hash_fn(NORMAL,data,&h,32)==0 && h==reference(data,32,0));
    h=0; assert(hash_fn(NORMAL,data,&h,27)==0 && h==reference(data,27,0));
    h=123; assert(hash_fn(NORMAL,data,&h,0)==0 && h==123);
    uint64_t rolling=reference(data,4096,0)^reference(data+512,4096,0)^reference(data+1024,8,0);
    h=0; assert(hash_fn(ROLLING,data,&h,sizeof(data))==0 && h==rolling);
    puts("case 2 normal tail rolling hash recurrence PASS");
    assert(numeric_fn("file2","file10",0)<0 && numeric_fn("file10","file2",0)>0);
    assert(numeric_fn("Ab2","ab10",1)==-1 && numeric_fn("ab10","Ab2",1)==1);
    assert(numeric_fn("Ab2","aB2",1)==0 && numeric_fn(NULL,"x",0)==JC_ENUMSTRCMP);
    assert(jc_streq("abc","abc")==0 && jc_streq("abc","abcd")!=0);
    assert(jc_strneq("a","b",0)==0 && jc_strcaseeq("AbC","aBc")==0);
    puts("case 3 numeric casefold suffix regression PASS");
    JC_STR_T *a=string_fn("abcdef",3),*b=string_fn("abc",0),*c=string_fn(NULL,123);
    assert(a && b && c && a->len==3 && b->len==3 && c->len==0);
    assert(!strcmp(a->str,"abc") && c->str[0]==0 && jc_strteq(a,b)==0);
    assert(jc_strtneq(a,b,0)==0 && string_fn("x",UINT32_MAX)==NULL);
    free(a);free(b);free(c);
    puts("case 4 owned prefixed C string boundaries PASS");
    char path[JC_PATHBUF_SIZE]="/a//b/.././c",relative[JC_PATHBUF_SIZE];
    assert(jc_collapse_dotdot(path)==0 && !strcmp(path,"/a/c"));
    assert(relative_fn("/a/b/source","/a/c/dest",relative)==0 && !strcmp(relative,"../b/source"));
    assert(relative_fn("/a/b/source","/a/b/source",relative)==1);
    assert(relative_fn(NULL,"/a/c/dest",relative)==JC_ENULL);
    assert(relative_fn("/a/b/source",NULL,relative)==JC_ENULL);
    puts("case 5 relative path status regression PASS");
    const unsigned char payload[]={0,0x7f,0x80,0xff,'\n','z',0}; unsigned char buf[sizeof(payload)];
    FILE *f=tmpfile(); assert(f); jc_errno=0;
    assert(jc_fwrite(payload,1,sizeof(payload),f)==sizeof(payload));
    assert(fflush(f)==0 && fseek(f,0,SEEK_SET)==0);
    assert(read_fn(buf,1,sizeof(buf),f)==sizeof(buf) && !memcmp(buf,payload,sizeof(buf)));
    assert(read_fn(buf,1,1,f)==0 && jc_feof(f)!=0 && jc_ferror(f)==0);
    jc_errno=0; assert(read_fn(NULL,1,1,f)==0 && jc_errno==EFAULT);
    jc_errno=0; assert(jc_ferror(NULL)==-1 && jc_errno==EFAULT);
    assert(jc_fclose(f)==0);
    puts("case 6 binary stdio EOF null errors PASS");
    puts("libjodycode six strict API cases PASS"); return 0;
}
C
cat > expected.stdout <<'EXPECTED'
case 1 actual ABI version numeric errors PASS
case 2 normal tail rolling hash recurrence PASS
case 3 numeric casefold suffix regression PASS
case 4 owned prefixed C string boundaries PASS
case 5 relative path status regression PASS
case 6 binary stdio EOF null errors PASS
libjodycode six strict API cases PASS
EXPECTED

%build
# Environment LDFLAGS preserves Makefile's append of its original SONAME.
export LDFLAGS="%{build_ldflags}"
%make_build CC=gcc CFLAGS_EXTRA="%{optflags}"
test -f libjodycode.a && test -f libjodycode.so.4.2.0 && test -f libjodycode.3.gz
readelf -d libjodycode.so.4.2.0 | grep -E '\(SONAME\).*\[libjodycode\.so\.4\]'
gcc %{optflags} -std=gnu11 -UNDEBUG -I. api-smoke.c -L. -ljodycode %{build_ldflags} -o api-smoke

%install
%make_install PREFIX=%{_prefix} LIB_DIR=%{_libdir} INC_DIR=%{_includedir} MAN3_DIR=%{_mandir}/man3
install -Dpm 0644 api-smoke.c %{buildroot}%{_datadir}/%{name}-tests/api-smoke.c
install -Dpm 0644 expected.stdout %{buildroot}%{_datadir}/%{name}-tests/expected.stdout

%check
(cd license-notices; sha256sum -c SHA256SUMS)
# Original target retained verbatim: one echo-OK script, zero functional asserts.
if %make_build test > original-test.stdout 2> original-test.stderr; then :; else status=$?; cat original-test.stdout original-test.stderr; exit "$status"; fi
cat original-test.stdout original-test.stderr
test "$(grep -cFx OK original-test.stdout)" -eq 1
test ! -s original-test.stderr
if LD_LIBRARY_PATH="$PWD" ./api-smoke > api.stdout 2> api.stderr; then :; else status=$?; cat api.stdout api.stderr; exit "$status"; fi
cat api.stdout; cmp expected.stdout api.stdout; test ! -s api.stderr
# RPM install-post has completed; bind the final actual installed bytes.
cd %{buildroot}
sha256sum usr/lib64/libjodycode.so.4.2.0 usr/lib64/libjodycode.a usr/include/libjodycode.h usr/share/man/man3/libjodycode.3.gz usr/share/libjodycode-tests/api-smoke.c usr/share/libjodycode-tests/expected.stdout > usr/share/libjodycode-tests/SHA256SUMS

%files
%license LICENSE.txt Public-Domain.notice Apache-2.0.txt license-notices
%doc README.md CHANGES.txt
%{_libdir}/libjodycode.so.4.2.0
%{_libdir}/libjodycode.so.4
%{_libdir}/libjodycode.so
%{_libdir}/libjodycode.a
%{_includedir}/libjodycode.h
%{_mandir}/man3/libjodycode.3.gz
%{_datadir}/%{name}-tests

%changelog
* Mon Oct 26 2026 openEuler RISC-V package contributors - 4.2-1
- Preserve default libraries/manual/dummy target with strict added consumers.

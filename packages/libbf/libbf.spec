# SPDX-License-Identifier: Apache-2.0
Name:           libbf
Version:        2025.06.03
Release:        1%{?dist}
Summary:        Arbitrary precision binary and decimal floating point library
License:        MIT AND Apache-2.0
URL:            https://bellard.org/libbf/
Source0:        libbf-2025-06-03.tar.gz
Source1:        Apache-2.0.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  time
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gcc
Requires:       glibc-devel
Requires:       grep

%description
LibBF provides arbitrary precision binary and decimal floating point
arithmetic. The original default bfbench, bfpi and bfcalc programs are
built and installed. The package additionally provides a static archive
and the public header for C consumers; upstream has no install or library
archive target. No shared library or pkg-config contract is invented.

%prep
%setup -q -n libbf-2025-06-03
find . -type f -print | LC_ALL=C sort > ../libbf-original-files.list
test "$(wc -l < ../libbf-original-files.list)" -eq 25
mkdir source-notices
while IFS= read -r item; do
    rel="${item#./}"
    cp -p "$item" "source-notices/$rel.notice"
    chmod 0644 "source-notices/$rel.notice"
done < ../libbf-original-files.list
(cd source-notices; sha256sum *.notice) > ../libbf-original-SHA256SUMS
mv ../libbf-original-SHA256SUMS source-notices/SHA256SUMS
test "$(wc -l < source-notices/SHA256SUMS)" -eq 25
cp -p %{SOURCE1} Apache-2.0.txt
cat > MIT.notice <<'NOTICE'
The original complete copyright, MIT grant, conditions and disclaimer are
retained verbatim with every original source file in source-notices/.
Eighteen source/header/Makefile notices contain the full MIT text. The
associated readme, VERSION and five original Pi-output digest files are
also retained byte-for-byte under the author's project MIT distribution.
readline.c additionally credits Charlie Gordon (2017-2024); those notices
are not replaced by a single-author summary. Algorithm/idea attributions
to GMP, MPFR and named papers remain in the original complete source.
NOTICE
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
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libbf.h>

static void (*volatile context_fn)(bf_context_t *,bf_realloc_func_t *,void *)=bf_context_init;
static int (*volatile parse_fn)(bf_t *,const char *,const char **,int,limb_t,bf_flags_t)=bf_atof;
static int (*volatile add_fn)(bf_t *,const bf_t *,const bf_t *,limb_t,bf_flags_t)=bf_add;
static int (*volatile divide_fn)(bf_t *,const bf_t *,const bf_t *,limb_t,bf_flags_t)=bf_div;
static int (*volatile decimal_fn)(bfdec_t *,const bfdec_t *,const bfdec_t *,limb_t,bf_flags_t)=bfdec_add;
static int (*volatile sqrtrem_fn)(bf_t *,bf_t *,const bf_t *)=bf_sqrtrem;

static void *resize(void *opaque,void *ptr,size_t size) {
    (void)opaque;
    if (size==0) { free(ptr); return NULL; }
    return realloc(ptr,size);
}
static int64_t integer(const bf_t *a) {
    int64_t value=0;
    assert(bf_get_int64(&value,a,0)==0);
    return value;
}
int main(void) {
    bf_context_t ctx;
    bf_t a,b,r,copy,remainder;
    context_fn(&ctx,resize,NULL);
    bf_init(&ctx,&a); bf_init(&ctx,&b); bf_init(&ctx,&r);
    bf_init(&ctx,&copy); bf_init(&ctx,&remainder);
    assert(bf_is_zero(&a) && a.sign==0 && a.tab==NULL);
    assert(bf_set_ui(&a,40)==0 && bf_set_ui(&b,2)==0);
    assert(add_fn(&r,&a,&b,128,BF_RNDN)==0 && integer(&r)==42);
    assert(bf_set(&copy,&r)==0 && bf_cmp_full(&copy,&r)==0);
    assert(bf_set_ui(&r,7)==0 && integer(&copy)==42);
    puts("case 1 context integer addition independent copy PASS");

    const char *end=NULL;
    const char *input="12345tail";
    assert(parse_fn(&a,input,&end,10,128,BF_RNDN)==0);
    assert(end==input+5 && !strcmp(end,"tail") && integer(&a)==12345);
    size_t length=0;
    char *formatted=bf_ftoa(&length,&a,10,128,BF_FTOA_FORMAT_FREE_MIN|BF_RNDN);
    assert(formatted!=NULL && length==5 && !strcmp(formatted,"12345"));
    bf_free(&ctx,formatted);
    puts("case 2 parse consumed suffix format ownership PASS");

    assert(bf_set_ui(&a,5)==0 && bf_set_ui(&b,2)==0);
    assert(divide_fn(&r,&a,&b,128,BF_RNDN)==0);
    assert(bf_set(&copy,&r)==0);
    assert(bf_rint(&r,BF_RNDN)==BF_ST_INEXACT && integer(&r)==2);
    assert(bf_rint(&copy,BF_RNDNA)==BF_ST_INEXACT && integer(&copy)==3);
    puts("case 3 exact division ties even ties away PASS");

    assert(bf_set_ui(&a,1)==0 && bf_set_ui(&b,0)==0);
    assert(divide_fn(&r,&a,&b,128,BF_RNDN)==BF_ST_DIVIDE_ZERO);
    assert(r.expn==BF_EXP_INF && r.sign==0);
    assert(bf_set_si(&a,-1)==0);
    assert(bf_sqrt(&r,&a,128,BF_RNDN)==BF_ST_INVALID_OP && bf_is_nan(&r));
    puts("case 4 divide zero invalid sqrt status PASS");

    bfdec_t da,db,dr,expected;
    bfdec_init(&ctx,&da); bfdec_init(&ctx,&db);
    bfdec_init(&ctx,&dr); bfdec_init(&ctx,&expected);
    assert(bfdec_atof(&da,"0.1",&end,34,BF_RNDN)==0 && *end=='\0');
    assert(bfdec_atof(&db,"0.2",&end,34,BF_RNDN)==0 && *end=='\0');
    assert(bfdec_atof(&expected,"0.3",&end,34,BF_RNDN)==0 && *end=='\0');
    assert(decimal_fn(&dr,&da,&db,34,BF_RNDN)==0 && bfdec_cmp_full(&dr,&expected)==0);
    formatted=bfdec_ftoa(&length,&dr,34,BF_FTOA_FORMAT_FREE|BF_RNDN);
    assert(formatted!=NULL && length==3 && !strcmp(formatted,"0.3"));
    bf_free(&ctx,formatted);
    bfdec_delete(&da); bfdec_delete(&db); bfdec_delete(&dr); bfdec_delete(&expected);
    puts("case 5 exact decimal addition format PASS");

    assert(bf_set_ui(&a,1)==0 && bf_mul_2exp(&a,200,BF_PREC_INF,BF_RNDZ)==0);
    assert(bf_add_si(&b,&a,7,BF_PREC_INF,BF_RNDZ)==0);
    assert(bf_sub(&r,&b,&a,BF_PREC_INF,BF_RNDZ)==0 && integer(&r)==7);
    assert(sqrtrem_fn(&r,&remainder,&a)==0 && bf_is_zero(&remainder));
    assert(bf_set_ui(&copy,1)==0 && bf_mul_2exp(&copy,100,BF_PREC_INF,BF_RNDZ)==0);
    assert(bf_cmp_full(&r,&copy)==0);
    bf_delete(&a); bf_delete(&b); bf_delete(&r); bf_delete(&copy); bf_delete(&remainder);
    bf_context_end(&ctx);
    puts("case 6 wide integer subtraction sqrt remainder PASS");
    puts("libbf six cases PASS");
    return 0;
}
C
cat > expected.stdout <<'EXPECTED'
case 1 context integer addition independent copy PASS
case 2 parse consumed suffix format ownership PASS
case 3 exact division ties even ties away PASS
case 4 divide zero invalid sqrt status PASS
case 5 exact decimal addition format PASS
case 6 wide integer subtraction sqrt remainder PASS
libbf six cases PASS
EXPECTED

%build
%make_build CFLAGS="%{optflags} -Wall -g -MMD" LDFLAGS="%{?build_ldflags}"
ar rcs libbf.a libbf.o cutils.o
gcc %{optflags} -UNDEBUG -I. api-smoke.c -L. -lbf -lm -o api-smoke

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_libdir} %{buildroot}%{_includedir}
install -m 0755 bfbench bfpi bfcalc %{buildroot}%{_bindir}/
install -m 0644 libbf.a %{buildroot}%{_libdir}/libbf.a
install -m 0644 libbf.h %{buildroot}%{_includedir}/libbf.h
install -d %{buildroot}%{_datadir}/libbf-tests
install -m 0644 api-smoke.c expected.stdout %{buildroot}%{_datadir}/libbf-tests/

%check
export LC_ALL=C
if make test CFLAGS="%{optflags} -Wall -g -MMD" LDFLAGS="%{?build_ldflags}" > upstream-test.log 2>&1; then
    cat upstream-test.log
else
    status=$?; cat upstream-test.log >&2; exit "$status"
fi
test "$(grep -c '^pi_1e[56]\.txt: OK$' upstream-test.log)" -eq 2
if ./api-smoke > api.stdout 2> api.stderr; then :; else
    status=$?; cat api.stdout api.stderr >&2; exit "$status"
fi
cmp expected.stdout api.stdout
test ! -s api.stderr
cat api.stdout
# RPM install-post has already stripped installed products before this phase.
(cd %{buildroot}; sha256sum usr/bin/bfbench usr/bin/bfpi usr/bin/bfcalc usr/lib64/libbf.a usr/include/libbf.h usr/share/libbf-tests/api-smoke.c usr/share/libbf-tests/expected.stdout) > %{buildroot}%{_datadir}/libbf-tests/SHA256SUMS

%files
%license MIT.notice Apache-2.0.txt source-notices
%doc readme.txt
%{_bindir}/bfbench
%{_bindir}/bfpi
%{_bindir}/bfcalc
%{_libdir}/libbf.a
%{_includedir}/libbf.h
%{_datadir}/libbf-tests/

%changelog
* Mon Oct 26 2026 openEuler RISC-V package contributors - 2025.06.03-1
- Package official dated source with original portable defaults and Pi tests.
- Add explicit static consumer archive/install contract and six strict cases.

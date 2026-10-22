# SPDX-License-Identifier: Apache-2.0
Name:           libenv
Version:        1.0.3.1
Release:        1
Summary:        Environment variable classification and filtering library
License:        ISC
URL:            https://codeberg.org/maandree/libenv
Source0:        https://codeberg.org/maandree/libenv/archive/%{version}.tar.gz
Patch0:         0001-pair-variadic-start-and-end.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils

%description
C library with a database of environment variable classifications and functions
to select or filter lists. Classifications are not a security-policy guarantee.

%package devel
Summary:        Headers, static library and manuals for libenv
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for linking with libenv.

%package tests
Summary:        Unchanged original source drivers for libenv checks
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       /bin/sh

%description tests
Checksum-bound original release for replaying both unchanged original drivers
and independent installed API tests. This is not security or native validation.

%prep
%autosetup -n libenv -p1

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall -Wextra" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -d %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/libenv.* %{buildroot}%{_libdir}/
rmdir %{buildroot}%{_prefix}/lib
install -d %{buildroot}%{_datadir}/libenv/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libenv/qa/libenv-%{version}.tar.gz

%check
make check CC="gcc -std=c99" CFLAGS="%{optflags} -Wall -Wextra" LDFLAGS="%{?build_ldflags}"
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libenv/qa/libenv-1.0.3.1.tar.gz"
    echo '17c49b55aec49277e0d99e27417d5e4327a5c359f13fcf7e73c3e68f41e5541e  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT HUP INT TERM
    tar -xzf "$archive" -C "$work"
    original="$work/libenv"
    libdir="$root/usr/lib64"
    export LD_LIBRARY_PATH="$libdir"
    # Unchanged original synthetic-table driver overrides only the table symbol.
    # Individual archive members resolve the remaining APIs from the packaged library.
    gcc -std=c99 -D_DEFAULT_SOURCE -I"$root/usr/include" -I"$original" -Wall -Wextra -o "$work/original-test-static" "$original/test.c" "$libdir/libenv.a"
    "$work/original-test-static"
    gcc -std=c99 -D_DEFAULT_SOURCE -I"$root/usr/include" -I"$original" -Wall -Wextra -o "$work/original-test-shared" "$original/test.c" -L"$libdir" -lenv
    "$work/original-test-shared"
    gcc -std=c99 -I"$root/usr/include" -Wall -Wextra -o "$work/variables-static" "$original/test-variables.c" "$libdir/libenv.a"
    "$work/variables-static"
    gcc -std=c99 -I"$root/usr/include" -Wall -Wextra -o "$work/variables-shared" "$original/test-variables.c" -L"$libdir" -lenv
    "$work/variables-shared"
    cat > "$work/consumer.c" <<'C'
#define _POSIX_C_SOURCE 200809L
#include <libenv.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const struct libenv_variable *table;
static size_t words, count;
typedef size_t (*CF)(const char **, ...);
typedef size_t (*CV)(const char **, va_list);
typedef size_t (*DF)(char **, ...);
typedef size_t (*DV)(char **, va_list);
static size_t cvcall(CV f, const char **a, ...) { va_list v; size_t n; va_start(v,a); n=f(a,v); va_end(v); return n; }
static size_t dvcall(DV f, char **a, ...) { va_list v; size_t n; va_start(v,a); n=f(a,v); va_end(v); return n; }
static const char **vchosen(enum libenv_class c, ...) { va_list v; const char **r; va_start(v,c); r=libenv_vget_chosen_list(c,v); va_end(v); return r; }
static int match(const char *s, int variable, const enum libenv_class *cls, int all)
{
    size_t i,j,k;
    for (i=0;i<count;i++) {
        k=strlen(table[i].name);
        if (strncmp(s,table[i].name,k) || s[k]!=(variable?'=':'\0')) continue;
        for (j=0;cls[j]!=LIBENV_END;j++) {
            size_t c=(size_t)cls[j];
            int yes=c/64<words && ((table[i].classes[c/64]>>(c%%64))&1);
            if (all && !yes) return 0;
            if (!all && yes) return 1;
        }
        return all;
    }
    return all && cls[0]==LIBENV_END;
}
int main(void)
{
    CF cf[]={libenv_filter_name_list,libenv_select_name_list,libenv_filter_variable_list,libenv_select_variable_list};
    CV cv[]={libenv_vfilter_name_list,libenv_vselect_name_list,libenv_vfilter_variable_list,libenv_vselect_variable_list};
    DF df[]={libenv_filter_name_list_with_dealloc,libenv_select_name_list_with_dealloc,libenv_filter_variable_list_with_dealloc,libenv_select_variable_list_with_dealloc};
    DV dv[]={libenv_vfilter_name_list_with_dealloc,libenv_vselect_name_list_with_dealloc,libenv_vfilter_variable_list_with_dealloc,libenv_vselect_variable_list_with_dealloc};
    const char *input[2][9]={{"DISPLAY","PATH","TERM","USER","UNSEEN","DISPLAYX","",NULL},{"DISPLAY=x","PATH=/a:/b","TERM=x","USER=z","UNSEEN=","DISPLAYX=x","DISPLAY","",NULL}};
    enum libenv_class cls[][3]={{LIBENV_END,LIBENV_END,LIBENV_END},{LIBENV_DISPLAY,LIBENV_END,LIBENV_END},{LIBENV_DISPLAY,LIBENV_PATH,LIBENV_END},{LIBENV_PATH,LIBENV_REMOTE_UNSAFE,LIBENV_END},{(enum libenv_class)100000,LIBENV_END,LIBENV_END}};
    size_t i,j,k,t,mode,n,expected,actual; const char *a[9]; char *d[9];
    table=libenv_get_complete_list(&words,&count); assert(table && words && count);
    assert(table==libenv_get_complete_list(NULL,NULL)); assert(!table[count].name && !table[count].classes);
    for(i=0;i<count;i++) { assert(table[i].name && *table[i].name && table[i].classes && !(table[i].classes[0]&1)); for(j=0;j<i;j++) assert(strcmp(table[i].name,table[j].name)); }
    for(k=0;k<4;k++) for(t=0;t<5;t++) for(mode=0;mode<4;mode++) {
        const char **in=input[k/2]; int all=!(k%%2); expected=0;
        for(n=0;in[n];n++) { a[n]=in[n]; d[n]=strdup(in[n]); assert(d[n]); }
        a[n]=NULL; d[n]=NULL;
        for(i=0;i<n;i++) if(all ^ match(in[i],k/2,cls[t],all)) expected++;
        if(mode==0) actual=cf[k](a,cls[t][0],cls[t][1],LIBENV_END);
        else if(mode==1) actual=cvcall(cv[k],a,cls[t][0],cls[t][1],LIBENV_END);
        else if(mode==2) actual=df[k](d,cls[t][0],cls[t][1],LIBENV_END);
        else actual=dvcall(dv[k],d,cls[t][0],cls[t][1],LIBENV_END);
        assert(actual==expected); j=0;
        for(i=0;i<n;i++) if(all ^ match(in[i],k/2,cls[t],all)) { assert(!strcmp(mode<2?a[j]:d[j],in[i])); j++; }
        assert(!(mode<2?a[j]:d[j]));
        for(i=0;d[i];i++) free(d[i]);
        if(mode==0) assert(!cf[k](NULL,cls[t][0],LIBENV_END));
        if(mode==1) assert(!cvcall(cv[k],NULL,cls[t][0],LIBENV_END));
        if(mode==2) assert(!df[k](NULL,cls[t][0],LIBENV_END));
        if(mode==3) assert(!dvcall(dv[k],NULL,cls[t][0],LIBENV_END));
    }
    for(t=0;t<5;t++) for(mode=0;mode<2;mode++) {
        const char **r=mode?vchosen(cls[t][0],cls[t][1],LIBENV_END):libenv_get_chosen_list(cls[t][0],cls[t][1],LIBENV_END);
        assert(r); j=0;
        for(i=0;i<count;i++) if(match(table[i].name,0,cls[t],0)) { assert(r[j] && !strcmp(r[j],table[i].name)); j++; }
        assert(!r[j]); free(r);
    }
    puts("PASS libenv all 19 public APIs, production table, const/owned lists, variadic/va_list, AND/OR/empty/unknown and NULL cases");
    return 0;
}
C
    gcc -std=c99 -I"$root/usr/include" -Wall -Wextra -Werror -o "$work/consumer-static" "$work/consumer.c" "$libdir/libenv.a"
    "$work/consumer-static"
    gcc -std=c99 -I"$root/usr/include" -Wall -Wextra -Werror -o "$work/consumer-shared" "$work/consumer.c" -L"$libdir" -lenv
    "$work/consumer-shared"
    echo 'PASS libenv unchanged original drivers and independent static/shared installed consumers'
)
run_installed_tests '%{buildroot}'

%files
%license LICENSE
%doc README
%{_libdir}/libenv.so.1
%{_libdir}/libenv.so.1.0

%files devel
%license LICENSE
%{_includedir}/libenv.h
%{_libdir}/libenv.a
%{_libdir}/libenv.so
%{_mandir}/man3/libenv*.3*
%{_mandir}/man3/enum_libenv_class.3*
%{_mandir}/man3/struct_libenv_variable.3*
%{_mandir}/man7/libenv.7*

%files tests
%license LICENSE
%{_datadir}/libenv/

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3.1-1
- Preserve default upstream build/tests and add installed static/shared API checks.

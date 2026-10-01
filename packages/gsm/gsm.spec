# SPDX-License-Identifier: Apache-2.0
Name:           gsm
Version:        1.0.24
Release:        1%{?dist}
Summary:        GSM 06.10 speech codec library and tools
License:        TU-Berlin-2.0
URL:            https://www.quut.com/gsm/
Source0:        gsm-%{version}.tar.gz
Patch0:         0001-use-32-bit-longword-on-lp64.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf

%description
The GSM 06.10 codec library encodes and decodes narrow-band speech. The
toast, untoast and tcat command-line tools are included.

%package devel
Summary:        Development files for the GSM 06.10 codec
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
The public header, static library, shared-library linker name and pkg-config
metadata for building applications with libgsm.

%prep
%autosetup -n gsm-1.0-pl24 -p1

%build
%make_build CC=gcc 'CCFLAGS=-c %{optflags} -fPIC -DNeedFunctionPrototypes=1 -Wall -Wno-comment'
gcc -shared %{build_ldflags} -Wl,-soname,libgsm.so.1 \
  -o lib/libgsm.so.1.%{version} \
  -Wl,--whole-archive lib/libgsm.a -Wl,--no-whole-archive
ln -s libgsm.so.1.%{version} lib/libgsm.so.1
ln -s libgsm.so.1 lib/libgsm.so

%install
install -Dpm0755 lib/libgsm.so.1.%{version} %{buildroot}%{_libdir}/libgsm.so.1.%{version}
ln -s libgsm.so.1.%{version} %{buildroot}%{_libdir}/libgsm.so.1
ln -s libgsm.so.1 %{buildroot}%{_libdir}/libgsm.so
install -Dpm0644 lib/libgsm.a %{buildroot}%{_libdir}/libgsm.a
install -Dpm0644 inc/gsm.h %{buildroot}%{_includedir}/gsm/gsm.h
install -Dpm0755 bin/toast %{buildroot}%{_bindir}/toast
ln -s toast %{buildroot}%{_bindir}/untoast
ln -s toast %{buildroot}%{_bindir}/tcat
install -Dpm0644 man/toast.1 %{buildroot}%{_mandir}/man1/toast.1
for page in gsm gsm_explode gsm_option gsm_print; do
  install -Dpm0644 man/${page}.3 %{buildroot}%{_mandir}/man3/${page}.3
done
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/gsm.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: gsm
Description: GSM 06.10 speech codec library
Version: %{version}
Libs: -L${libdir} -lgsm
Cflags: -I${includedir}/gsm
EOF

%check
# Upstream's ETSI vectors are not redistributable and its tst/run exits 0
# when they are absent. Run the shipped arithmetic fixture explicitly and
# treat mismatch diagnostics as failure; add a public encode/decode check.
%make_build add-test/add CC=gcc 'CCFLAGS=-c %{optflags} -DNeedFunctionPrototypes=1 -Wall -Wno-comment'
add-test/add < add-test/add_test.dta > add-test-output.txt 2> add-test-errors.txt
if grep -F ' != ' add-test-errors.txt; then
  echo 'GSM arithmetic fixture mismatch' >&2
  exit 1
fi
cat > gsm-api-check.c <<'EOF'
#include <gsm.h>
int main(void) {
    gsm encoder = gsm_create(), decoder = gsm_create();
    gsm_signal input[160], output[160];
    gsm_byte frame[33];
    int nonzero = 0;
    if (!encoder || !decoder) return 1;
    for (int i = 0; i < 160; ++i) input[i] = (gsm_signal)((i % 80 - 40) * 128);
    gsm_encode(encoder, input, frame);
    if ((frame[0] >> 4) != GSM_MAGIC) return 2;
    if (gsm_decode(decoder, frame, output) != 0) return 3;
    for (int i = 0; i < 160; ++i) nonzero |= output[i];
    gsm_destroy(encoder);
    gsm_destroy(decoder);
    return nonzero == 0;
}
EOF
gcc %{optflags} -Iinc gsm-api-check.c -Llib -Wl,-rpath,$PWD/lib -lgsm -o gsm-api-check
./gsm-api-check

%files
%license COPYRIGHT
%doc README ChangeLog
%{_bindir}/toast
%{_bindir}/untoast
%{_bindir}/tcat
%{_libdir}/libgsm.so.1*
%{_mandir}/man1/toast.1*

%files devel
%license COPYRIGHT
%{_includedir}/gsm/gsm.h
%{_libdir}/libgsm.a
%{_libdir}/libgsm.so
%{_libdir}/pkgconfig/gsm.pc
%{_mandir}/man3/gsm.3*
%{_mandir}/man3/gsm_explode.3*
%{_mandir}/man3/gsm_option.3*
%{_mandir}/man3/gsm_print.3*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.24-1
- Initial openEuler RISC-V package with fixed-width codec arithmetic.

# SPDX-License-Identifier: Apache-2.0
Name:           liba53
Version:        4.0.0
Release:        1%{?dist}
%global upstream_commit efe146ece29c986c975398da92dd5e53f6319e0a
Summary:        GSM A5 and GEA cipher library
License:        GPL-2.0-or-later
URL:            https://github.com/RangeNetworks/liba53
Source0:        liba53-%{version}.tar.gz
Patch0:         0001-gea-test-use-direction-enum.patch

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
liba53 provides implementations of GSM A5, KASUMI, and GEA cipher functions.

%package devel
Summary:        Development files for liba53
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
The public C++ header, linker name, and pkg-config metadata for developing
applications with liba53.

%prep
%autosetup -n liba53-%{upstream_commit} -p1

%build
# Upstream's Makefile hard-codes compiler flags and /usr/lib; compile the same
# source set with openEuler hardening flags and install explicitly below.
g++ %{optflags} -fPIC -c a5.c bits.c gea.c kasumi.c utils.c ifc.cpp
g++ -shared %{build_ldflags} -Wl,-soname,liba53.so.1 \
  -o liba53.so.1.0 a5.o bits.o gea.o kasumi.o utils.o ifc.o
ln -s liba53.so.1.0 liba53.so.1
ln -s liba53.so.1 liba53.so

%install
install -Dpm0755 liba53.so.1.0 %{buildroot}%{_libdir}/liba53.so.1.0
ln -s liba53.so.1.0 %{buildroot}%{_libdir}/liba53.so.1
ln -s liba53.so.1 %{buildroot}%{_libdir}/liba53.so
install -Dpm0644 a53.h %{buildroot}%{_includedir}/a53.h
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/liba53.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: liba53
Description: GSM A5 and GEA cipher library
Version: %{version}
Libs: -L${libdir} -la53
Cflags: -I${includedir}
EOF

%check
# The upstream Makefile leaves its fixture targets commented out. Run every
# shipped vector program, checking their output against all three .ok files.
# a53test returns zero even on mismatches; explicitly inspect all 18 results.
g++ %{optflags} -include ctime -I. a53test.cpp -L. -Wl,-rpath,$PWD -la53 -o a53test
./a53test > a53test.out
test "$(grep -c ' ok$' a53test.out)" -eq 18
if grep -F ' ERROR' a53test.out; then
  echo 'A5/3 test vector mismatch' >&2
  exit 1
fi
for suite in a5_test kasumi_test gea_test; do
  g++ %{optflags} -I. ${suite}.c -L. -Wl,-rpath,$PWD -la53 -o ${suite}
  ./${suite} > ${suite}.out
  diff -u ${suite}.ok ${suite}.out
done

%files
%license COPYING
%doc README ChangeLog
%{_libdir}/liba53.so.1*

%files devel
%license COPYING
%{_includedir}/a53.h
%{_libdir}/liba53.so
%{_libdir}/pkgconfig/liba53.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.0-1
- Initial openEuler RISC-V package with all shipped cipher vector programs.

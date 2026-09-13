# SPDX-License-Identifier: Apache-2.0
Name:           libb64
Version:        2.0.0.1
Release:        1%{?dist}
Summary:        Base64 encoding and decoding library
License:        Public Domain
URL:            https://github.com/libb64/libb64
Source0:        libb64-2.0.0.1.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
libb64 provides ANSI C and C++ routines for Base64 encoding and decoding.

%package devel
Summary:        Development files for libb64
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and the static library for applications using libb64.

%prep
%autosetup -p1

%build
%make_build -C src CFLAGS="%{optflags} -I../include"
%make_build -C base64 CFLAGS="%{optflags} -I../include -DBUFFERSIZE=16777216" \
  CXXFLAGS="%{optflags} -I../include -DBUFFERSIZE=16777216"
%make_build -C examples CFLAGS="%{optflags} -I../include"

%install
install -Dpm0755 base64/base64 %{buildroot}%{_bindir}/b64
install -Dpm0644 src/libb64.a %{buildroot}%{_libdir}/libb64.a
install -dpm0755 %{buildroot}%{_includedir}/b64
install -pm0644 include/b64/*.h %{buildroot}%{_includedir}/b64/

%check
%make_build -C examples test CFLAGS="%{optflags}"

%files
%license LICENSE*
%doc README.md AUTHORS.md CHANGELOG.md
%{_bindir}/b64

%files devel
%license LICENSE*
%{_includedir}/b64/
%{_libdir}/libb64.a

%changelog
* Wed Aug 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0.1-1
- Package libb64 with its upstream example regression tests.

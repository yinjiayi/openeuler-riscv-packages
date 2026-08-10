# SPDX-License-Identifier: Apache-2.0
Name:           bearssl
Version:        0.6
Release:        1%{?dist}
Summary:        Small implementation of TLS in C
License:        MIT
URL:            https://www.bearssl.org/
Source0:        bearssl-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
BearSSL is a small implementation of the SSL/TLS protocol written in C. This
package contains the brssl command-line tool.

%package devel
Summary:        Development files for BearSSL

%description devel
Header files and the static library for developing applications with BearSSL.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  LD=%{__cc} \
  CFLAGS='%{optflags} -fPIC -Wall' \
  LDFLAGS='%{__global_ldflags}' \
  lib tools tests

%install
install -D -m 0755 build/brssl %{buildroot}%{_bindir}/brssl
install -D -m 0644 build/libbearssl.a %{buildroot}%{_libdir}/libbearssl.a
install -d -m 0755 %{buildroot}%{_includedir}/bearssl
install -m 0644 inc/*.h %{buildroot}%{_includedir}/bearssl/

%check
./build/testcrypto all

%files
%license LICENSE.txt
%doc README.txt
%{_bindir}/brssl

%files devel
%license LICENSE.txt
%{_includedir}/bearssl/
%{_libdir}/libbearssl.a

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6-1
- Initial openEuler RISC-V package.

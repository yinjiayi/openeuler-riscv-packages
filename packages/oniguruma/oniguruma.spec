# SPDX-License-Identifier: Apache-2.0
Name:           oniguruma
Version:        6.9.10
Release:        1%{?dist}
Summary:        Regular expression library supporting multiple encodings
License:        BSD-2-Clause
URL:            https://github.com/kkos/oniguruma
Source0:        onig-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Oniguruma is a regular expression library that supports many character
encodings and language-specific regular expression syntaxes.

%package devel
Summary:        Development files for Oniguruma
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, the onig-config helper, and the unversioned
library link for developing applications with Oniguruma.

%prep
%autosetup -n onig-%{version} -p1

%build
%configure \
  --disable-static \
  --enable-posix-api \
  --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS HISTORY NEWS README.md
%{_libdir}/libonig.so.5*

%files devel
%license COPYING
%{_bindir}/onig-config
%{_includedir}/onig*.h
%{_libdir}/libonig.so
%{_libdir}/pkgconfig/oniguruma.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.9.10-1
- Initial openEuler RISC-V package with POSIX API and upstream tests.

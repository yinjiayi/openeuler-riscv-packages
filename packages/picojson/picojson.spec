# SPDX-License-Identifier: Apache-2.0
Name:           picojson
Version:        1.3.0
Release:        1%{?dist}
Summary:        Header-only JSON parser and serializer for C++
License:        BSD-2-Clause
URL:            https://github.com/kazuho/picojson
Source0:        picojson-1.3.0.tar.gz
BuildArch:      noarch

BuildRequires:  gcc-c++
BuildRequires:  make

%description
PicoJSON is a small, header-only JSON parser and serializer for C++.

%prep
%autosetup -p1

%build
# Header-only library; compilation is exercised in %%check.

%install
%make_install prefix=%{_prefix} includedir=%{_includedir}

%check
%make_build check CXX=%{__cxx}

%files
%license LICENSE
%doc Changes README.mkdn
%{_includedir}/picojson.h

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package.


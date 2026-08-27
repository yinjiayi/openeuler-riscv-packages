# SPDX-License-Identifier: Apache-2.0
Name:           kyua
Version:        0.13
Release:        1%{?dist}
Summary:        Collection of libraries and tools to implement and run automated tests
License:        BSD-3-Clause
URL:            https://github.com/jmmv/kyua
Source0:        kyua-0.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Collection of libraries and tools to implement and run automated tests

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc NEWS.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Initial openEuler RISC-V package from the full package inventory.

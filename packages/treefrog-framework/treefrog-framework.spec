# SPDX-License-Identifier: Apache-2.0
Name:           treefrog-framework
Version:        2.12.0
Release:        1%{?dist}
Summary:        High-speed C++ MVC Framework for Web Application
License:        BSD-3-Clause
URL:            https://github.com/treefrogframework/treefrog-framework
Source0:        treefrog-framework-2.12.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
High-speed C++ MVC Framework for Web Application

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license copyright
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-1
- Initial openEuler RISC-V package from the full package inventory.

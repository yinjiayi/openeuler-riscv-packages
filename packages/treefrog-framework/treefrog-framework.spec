# SPDX-License-Identifier: Apache-2.0
Name:           treefrog-framework
Version:        2.12.0
Release:        4%{?dist}
Summary:        High-speed C++ MVC Framework for Web Application
License:        BSD-3-Clause
URL:            https://github.com/treefrogframework/treefrog-framework
Source0:        treefrog-framework-2.12.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  mongo-c-driver-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel

%description
High-speed C++ MVC Framework for Web Application

%prep
%autosetup -p1

%build
%set_build_flags
./configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir}/treefrog \
  --datadir=%{_datadir}/treefrog \
  --enable-shared-mongoc
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license copyright
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-4
- Use the repository MongoDB C driver instead of rebuilding the bundled copy.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-3
- Add the Qt 6 QML development module required by TreeFrog's qmake project.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-2
- Use TreeFrog's supported configure interface and declare its build tools.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12.0-1
- Initial openEuler RISC-V package from the full package inventory.

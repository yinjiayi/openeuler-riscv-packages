# SPDX-License-Identifier: Apache-2.0
Name:           termox
Version:        2.0.0
Release:        3%{?dist}
Summary:        C++17 Terminal User Interface(TUI) Library.
License:        MIT
URL:            https://github.com/a-n-t-h-o-n-y/TermOx
Source0:        termox-2.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libicu-devel
BuildRequires:  make

%description
C++17 Terminal User Interface(TUI) Library.

%prep
%autosetup -n TermOx-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir}
%cmake_build
%cmake_build --target TermOx.tests.unit

%install
install -Dpm 0644 %{_vpath_builddir}/libTermOx.a %{buildroot}%{_libdir}/libTermOx.a
install -d %{buildroot}%{_includedir}
cp -a include/ox %{buildroot}%{_includedir}/
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/tests/TermOx.tests.unit

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-3
- Add the ICU development dependency required by the pinned Escape subproject.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-2
- Fix the case-sensitive source root and build the upstream unit target.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.

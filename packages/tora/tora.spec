# SPDX-License-Identifier: Apache-2.0
Name:           tora
Version:        3.2
Release:        7%{?dist}
Summary:        SQL IDE for Oracle, MySQL and PostgreSQL dbs
License:        GPL-2.0-or-later
URL:            https://github.com/tora-tool/tora
Source0:        tora-3.2.tar.gz
Patch0:         0001-stack-support-riscv-backtrace.patch
Patch1:         0002-dtl-fix-const-mutator.patch
Patch2:         0003-include-qmenu-definition.patch
Patch3:         0004-antlr-fix-cyclic-dfa-copy.patch
BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  boost-system
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qscintilla-qt5-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel

%description
SQL IDE for Oracle, MySQL and PostgreSQL dbs

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON -DWANT_INTERNAL_LOKI=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING
%license COPYING.RTF
%license copyright.txt
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Sun Aug 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-7
- Fix immutable CyclicDFA copy operations in the bundled ANTLR3 C++ runtime.

* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-6
- Include the QMenu definition before calling its methods.

* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-5
- Fix the bundled DTL const mutator rejected by GCC 14.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-4
- Implement RISC-V stack collection with the glibc backtrace interfaces.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-3
- Use the bundled Loki headers and add the Qt 5 and QScintilla development dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-2
- Add the Boost headers and system library required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2-1
- Initial openEuler RISC-V package from the full package inventory.

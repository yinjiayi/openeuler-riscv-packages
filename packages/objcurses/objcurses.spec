# SPDX-License-Identifier: Apache-2.0
Name:           objcurses
Version:        1.3.0
Release:        2%{?dist}
Summary:        Minimalistic 3D object viewer for the terminal using ncurses
License:        MIT
URL:            https://github.com/admtrv/objcurses
Source0:        objcurses-1.3.0.tar.gz
Patch0:         patches/0001-cmake-exclude-compiler-probes.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
Minimalistic 3D object viewer for the terminal using ncurses

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
install -Dpm 0755 %{_vpath_builddir}/objcurses %{buildroot}%{_bindir}/objcurses

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files
%{_bindir}/objcurses
%license LICENSE.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-2
- Install the executable explicitly because upstream has no CMake install rule.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Curses headers and library required by CMake.
- Exclude CMake compiler probes from the recursive source glob.

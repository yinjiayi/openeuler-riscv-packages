# SPDX-License-Identifier: Apache-2.0
Name:           qucs-rflayout
Version:        2.1.2
Release:        5%{?dist}
Summary:        Export Qucs RF schematics to KiCad layouts & OpenEMS scripts
License:        GPL-3.0-or-later
URL:            https://github.com/thomaslepoix/Qucs-RFlayout
Source0:        qucs-rflayout-2.1.2.tar.gz
Patch0:         0001-cmake-guard-optional-latex-docs.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  qt6-qtbase-devel

%description
Export Qucs RF schematics to KiCad layouts & OpenEMS scripts

%prep
%autosetup -n Qucs-RFlayout-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
# Upstream's install hook runs "make gzip" relative to the current directory.
(
  cd %{_vpath_builddir}
  DESTDIR=%{buildroot} cmake --install .
)
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%cmake_build --target check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-5
- Run installation in the build directory required by the gzip document hook.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-4
- Build optional LaTeX diagrams only when XeLaTeX is available, while retaining
  the complete GUI product and Catch test targets.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-3
- Configure the explicit out-of-tree directory expected by the build, install,
  and upstream check macros.
- Exercise the installed command-line version entry point in smoke testing.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-2
- Match the official archive root and add the Qt 6 and OpenGL development files.
- Run the upstream check target so its excluded unit-test executable is built before CTest.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Initial openEuler RISC-V package from the full package inventory.

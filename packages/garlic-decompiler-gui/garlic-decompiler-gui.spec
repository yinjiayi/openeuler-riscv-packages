# SPDX-License-Identifier: Apache-2.0
Name:           garlic-decompiler-gui
Version:        1.1.0
Release:        2%{?dist}
Summary:        Gui for the Garlic Decompiler, supporting APK, DEX, JAR, and CLASS decompilation
License:        Apache-2.0
URL:            https://github.com/AgarwalKritik/garlic-gui
Source0:        garlic-decompiler-gui-1.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  qt6-qtbase-devel

%description
Gui for the Garlic Decompiler, supporting APK, DEX, JAR, and CLASS decompilation

%prep
%autosetup -n garlic-gui-%{version} -p1

%build
%cmake -DBUILD_TESTING=ON -DGARLIC_STATIC_QT=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-2
- Use the upstream archive root and build against distribution Qt 6.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.

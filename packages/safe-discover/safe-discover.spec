# SPDX-License-Identifier: Apache-2.0
Name:           safe-discover
Version:        0.2.1
Release:        3%{?dist}
Summary:        Kirigami-based package management GUI for Arch Linux (pacman, AUR, Flatpak, fwupd)
License:        GPL-3.0-or-later
URL:            https://github.com/kinncj/Safe-Discover
Source0:        safe-discover-0.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Kirigami-based package management GUI for Arch Linux (pacman, AUR, Flatpak, fwupd)

%prep
%autosetup -n Safe-Discover-%{version} -p1

%build
%cmake -DBUILD_TESTING=ON
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
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-3
- Declare the Extra CMake Modules dependency required by upstream configuration.

* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-2
- Match %%prep to the case-sensitive upstream release archive root.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.

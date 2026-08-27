# SPDX-License-Identifier: Apache-2.0
Name:           jellyfin-media-player
Version:        1.12.0
Release:        1%{?dist}
Summary:        Jellyfin Desktop Client - Legacy
License:        GPL-2.0-or-later
URL:            https://github.com/jellyfin-archive/jellyfin-desktop-qt
Source0:        jellyfin-media-player-1.12.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Jellyfin Desktop Client - Legacy

%prep
%autosetup -p1

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.0-1
- Initial openEuler RISC-V package from the full package inventory.

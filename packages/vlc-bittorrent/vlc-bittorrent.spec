# SPDX-License-Identifier: Apache-2.0
Name:           vlc-bittorrent
Version:        2.16
Release:        1%{?dist}
Summary:        A bittorrent plugin for VLC.
License:        GPL-3.0-or-later
URL:            https://github.com/johang/vlc-bittorrent
Source0:        vlc-bittorrent-2.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A bittorrent plugin for VLC.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.16-1
- Initial openEuler RISC-V package from the full package inventory.

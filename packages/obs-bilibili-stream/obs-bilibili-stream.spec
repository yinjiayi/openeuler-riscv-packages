# SPDX-License-Identifier: Apache-2.0
Name:           obs-bilibili-stream
Version:        2.0.12
Release:        1%{?dist}
Summary:        Bilibili stream plugin for OBS Studio (Scan QR code to login, update room info, and get RTMP info)
License:        GPL-2.0-or-later
URL:            https://github.com/Zarosmm/obs-bilibili-stream
Source0:        obs-bilibili-stream-2.0.12.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Bilibili stream plugin for OBS Studio (Scan QR code to login, update room info, and get RTMP info)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.12-1
- Initial openEuler RISC-V package from the full package inventory.

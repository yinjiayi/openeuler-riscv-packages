# SPDX-License-Identifier: Apache-2.0
Name:           media-downloader
Version:        5.6.3
Release:        2%{?dist}
Summary:        A Qt/C++ front end to yt-dlp, youtube-dl, gallery-dl, lux, you-get, svtplay-dl, aria2c, wget and safari books.
License:        GPL-2.0-or-later
URL:            https://github.com/mhogomchungu/media-downloader
Source0:        media-downloader-5.6.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel

%description
A Qt/C++ front end to yt-dlp, youtube-dl, gallery-dl, lux, you-get, svtplay-dl, aria2c, wget and safari books.

%prep
%autosetup -p1

%build
%cmake -DBUILD_WITH_QT6=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%license LICENSE.txt
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.6.3-2
- Add the Qt 6 development dependency required by upstream CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.6.3-1
- Initial openEuler RISC-V package from the full package inventory.

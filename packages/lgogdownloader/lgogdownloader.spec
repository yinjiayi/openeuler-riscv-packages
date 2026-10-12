# SPDX-License-Identifier: Apache-2.0
Name:           lgogdownloader
Version:        3.18
Release:        1%{?dist}
Summary:        Open source downloader for GOG.com games, uses the GOG.com API
License:        WTFPL
URL:            https://github.com/Sude-/lgogdownloader
Source0:        lgogdownloader-3.18.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Open source downloader for GOG.com games, uses the GOG.com API

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.18-1
- Initial openEuler RISC-V package from the full package inventory.

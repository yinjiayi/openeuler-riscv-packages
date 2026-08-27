# SPDX-License-Identifier: Apache-2.0
Name:           obs-multi-rtmp
Version:        0.7.3.2
Release:        1%{?dist}
Summary:        Multiple RTMP outputs plugin for OBS Studio
License:        GPL-2.0-or-later
URL:            https://github.com/sorayuki/obs-multi-rtmp
Source0:        obs-multi-rtmp-0.7.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Multiple RTMP outputs plugin for OBS Studio

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.3.2-1
- Initial openEuler RISC-V package from the full package inventory.

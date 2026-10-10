# SPDX-License-Identifier: Apache-2.0
Name:           linux-fireface-mixer
Version:        0.4.0
Release:        1%{?dist}
Summary:        GUI mixer and headless OSC daemon for RME Fireface 400 on Linux
License:        GPL-3.0-or-later
URL:            https://github.com/oudeis01/linux-fireface-mixer
Source0:        linux-fireface-mixer-0.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GUI mixer and headless OSC daemon for RME Fireface 400 on Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.

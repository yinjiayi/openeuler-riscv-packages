# SPDX-License-Identifier: Apache-2.0
Name:           headsetcontrol
Version:        3.1.0
Release:        1%{?dist}
Summary:        Sidetone control and battery readout for gaming headsets
License:        GPL-3.0-or-later
URL:            https://github.com/Sapd/HeadsetControl
Source0:        headsetcontrol-3.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Sidetone control and battery readout for gaming headsets

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
%license license
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.0-1
- Initial openEuler RISC-V package from the full package inventory.

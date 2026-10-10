# SPDX-License-Identifier: Apache-2.0
Name:           clightd
Version:        5.9
Release:        1%{?dist}
Summary:        Bus interface to change screen brightness and capture frames from webcam.
License:        GPL-3.0-or-later
URL:            https://github.com/FedeDP/Clightd
Source0:        clightd-5.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Bus interface to change screen brightness and capture frames from webcam.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.9-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           qrookie-vrp
Version:        0.4.2
Release:        1%{?dist}
Summary:        Download and install Quest games from ROOKIE Public Mirror
License:        GPL-3.0-or-later
URL:            https://github.com/glaumar/QRookie
Source0:        qrookie-vrp-0.4.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Download and install Quest games from ROOKIE Public Mirror

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.2-1
- Initial openEuler RISC-V package from the full package inventory.

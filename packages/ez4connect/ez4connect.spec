# SPDX-License-Identifier: Apache-2.0
Name:           ez4connect
Version:        1.8.1
Release:        1%{?dist}
Summary:        Imporved Qt-based ZJU-Connect GUI
License:        GPL-3.0-or-later
URL:            https://github.com/chenx-dust/EZ4Connect
Source0:        ez4connect-1.8.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Imporved Qt-based ZJU-Connect GUI

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.1-1
- Initial openEuler RISC-V package from the full package inventory.

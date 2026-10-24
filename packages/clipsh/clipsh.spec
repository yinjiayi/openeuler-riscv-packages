# SPDX-License-Identifier: Apache-2.0
Name:           clipsh
Version:        1.0.5
Release:        1%{?dist}
Summary:        Qt6 QML plugin for managing clipboard history via cliphist
License:        MIT
URL:            https://github.com/Happilli/clipsh
Source0:        clipsh-1.0.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt6 QML plugin for managing clipboard history via cliphist

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           sysinfoviewer
Version:        0.3.2
Release:        1%{?dist}
Summary:        A comprehensive system information viewer built with wxWidgets
License:        MIT
URL:            https://github.com/Magpiny/sysinfoviewer
Source0:        sysinfoviewer-0.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A comprehensive system information viewer built with wxWidgets

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Initial openEuler RISC-V package from the full package inventory.

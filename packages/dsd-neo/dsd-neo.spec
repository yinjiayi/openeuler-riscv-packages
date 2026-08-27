# SPDX-License-Identifier: Apache-2.0
Name:           dsd-neo
Version:        2.5.1
Release:        1%{?dist}
Summary:        Digital Speech Decoder - A modern, modular, and performance enhanced C/C++ decoder for digital voice. DMR, P25, NXDN, YSF, and more.
License:        GPL-3.0-or-later
URL:            https://github.com/arancormonk/dsd-neo
Source0:        dsd-neo-2.5.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Digital Speech Decoder - A modern, modular, and performance enhanced C/C++ decoder for digital voice. DMR, P25, NXDN, YSF, and more.

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
%license COPYRIGHT
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-1
- Initial openEuler RISC-V package from the full package inventory.

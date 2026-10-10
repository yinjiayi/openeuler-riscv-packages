# SPDX-License-Identifier: Apache-2.0
Name:           keyfinder-cli
Version:        1.2.0
Release:        1%{?dist}
Summary:        Estimate the musical key of many different audio file formats
License:        GPL-3.0-or-later
URL:            https://github.com/evanpurkhiser/keyfinder-cli
Source0:        keyfinder-cli-1.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Estimate the musical key of many different audio file formats

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.

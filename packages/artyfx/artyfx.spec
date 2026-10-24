# SPDX-License-Identifier: Apache-2.0
Name:           artyfx
Version:        1.3.1
Release:        1%{?dist}
Summary:        A plugin bundle of artistic real-time audio effects
License:        GPL-2.0-or-later
URL:            https://github.com/openavproductions/openav-artyfx
Source0:        artyfx-1.3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A plugin bundle of artistic real-time audio effects

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
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Initial openEuler RISC-V package from the full package inventory.

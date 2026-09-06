# SPDX-License-Identifier: Apache-2.0
Name:           fabla
Version:        1.4
Release:        1%{?dist}
Summary:        An open-source LV2 drum sampler plugin instrument
License:        GPL-2.0-or-later
URL:            https://github.com/openavproductions/openav-fabla
Source0:        fabla-1.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An open-source LV2 drum sampler plugin instrument

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           obs-composite-blur
Version:        1.5.2
Release:        1%{?dist}
Summary:        Comprehensive blur plugin for OBS that provides several different blur algorithms, and proper compositing
License:        GPL-2.0-or-later
URL:            https://github.com/FiniteSingularity/obs-composite-blur
Source0:        obs-composite-blur-1.5.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Comprehensive blur plugin for OBS that provides several different blur algorithms, and proper compositing

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.2-1
- Initial openEuler RISC-V package from the full package inventory.

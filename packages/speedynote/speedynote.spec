# SPDX-License-Identifier: Apache-2.0
Name:           speedynote
Version:        1.5.1
Release:        1%{?dist}
Summary:        Fast note-taking app with PDF annotation, export, and multi-platform sync
License:        GPL-3.0-or-later
URL:            https://github.com/alpha-liu-01/SpeedyNote
Source0:        speedynote-1.5.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast note-taking app with PDF annotation, export, and multi-platform sync

%prep
%autosetup -n SpeedyNote-%{version} -p1

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.

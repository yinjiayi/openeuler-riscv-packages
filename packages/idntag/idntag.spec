# SPDX-License-Identifier: Apache-2.0
Name:           idntag
Version:        2.02
Release:        1%{?dist}
Summary:        Automatically identify, tag and rename audio files
License:        MIT
URL:            https://github.com/d99kris/idntag
Source0:        idntag-2.02.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Automatically identify, tag and rename audio files

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.02-1
- Initial openEuler RISC-V package from the full package inventory.

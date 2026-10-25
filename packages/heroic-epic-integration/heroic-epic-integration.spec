# SPDX-License-Identifier: Apache-2.0
Name:           heroic-epic-integration
Version:        0.4
Release:        1%{?dist}
Summary:        Epic Games Windows integration for Heroic
License:        MIT
URL:            https://github.com/Etaash-mathamsetty/heroic-epic-integration
Source0:        heroic-epic-integration-0.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Epic Games Windows integration for Heroic

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Initial openEuler RISC-V package from the full package inventory.

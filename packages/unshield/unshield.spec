# SPDX-License-Identifier: Apache-2.0
Name:           unshield
Version:        1.6.2
Release:        1%{?dist}
Summary:        Extracts CAB files from InstallShield installers
License:        MIT
URL:            https://github.com/twogood/unshield
Source0:        unshield-1.6.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Extracts CAB files from InstallShield installers

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
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-1
- Initial openEuler RISC-V package from the full package inventory.

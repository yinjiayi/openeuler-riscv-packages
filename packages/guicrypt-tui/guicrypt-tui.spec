# SPDX-License-Identifier: Apache-2.0
Name:           guicrypt-tui
Version:        1.1.0
Release:        1%{?dist}
Summary:        TUI manager for gocryptfs encrypted vaults
License:        MIT
URL:            https://github.com/guirossibrum/guicrypt-tui
Source0:        guicrypt-tui-1.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
TUI manager for gocryptfs encrypted vaults

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.

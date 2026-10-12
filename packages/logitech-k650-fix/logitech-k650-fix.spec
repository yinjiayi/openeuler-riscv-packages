# SPDX-License-Identifier: Apache-2.0
Name:           logitech-k650-fix
Version:        0.9.3
Release:        1%{?dist}
Summary:        Fix(insert key) Logitech K650 keyboard.
License:        MIT
URL:            https://github.com/bokic/logitech-k650-fix
Source0:        logitech-k650-fix-0.9.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Fix(insert key) Logitech K650 keyboard.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.3-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           thinkfan
Version:        2.0.0
Release:        1%{?dist}
Summary:        A minimalist fan control program. Supports the sysfs hwmon interface and thinkpad_acpi
License:        GPL-3.0-or-later
URL:            https://github.com/vmatare/thinkfan
Source0:        thinkfan-2.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A minimalist fan control program. Supports the sysfs hwmon interface and thinkpad_acpi

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.

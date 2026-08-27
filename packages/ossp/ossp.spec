# SPDX-License-Identifier: Apache-2.0
Name:           ossp
Version:        1.3.3
Release:        1%{?dist}
Summary:        Emulate OSS device using CUSE
License:        GPL-2.0-or-later
URL:            https://github.com/OpenMandrivaSoftware/ossp
Source0:        ossp-1.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Emulate OSS device using CUSE

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
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.3-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           opengate
Version:        9.4
Release:        1%{?dist}
Summary:        Open GATE - numerical simulations in medical imaging and radiotherapy
License:        LGPL-3.0-or-later
URL:            https://github.com/OpenGATE/Gate
Source0:        opengate-9.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Open GATE - numerical simulations in medical imaging and radiotherapy

%prep
%autosetup -n Gate-%{version} -p1

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
%license LICENSE.md
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 9.4-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           eprosima-fast-dds-statistics-backend
Version:        2.4.0
Release:        1%{?dist}
Summary:        eProsima Fast DDS Statistics Backend is a C++ library that provides collection and procession the statistics measurements reported by Fast DDS Statistics Mo
License:        Apache-2.0
URL:            https://github.com/eProsima/Fast-DDS-statistics-backend
Source0:        eprosima-fast-dds-statistics-backend-2.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
eProsima Fast DDS Statistics Backend is a C++ library that provides collection and procession the statistics measurements reported by Fast DDS Statistics Mo

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.0-1
- Initial openEuler RISC-V package from the full package inventory.

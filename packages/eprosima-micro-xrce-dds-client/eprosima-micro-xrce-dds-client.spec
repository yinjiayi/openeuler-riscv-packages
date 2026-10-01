# SPDX-License-Identifier: Apache-2.0
Name:           eprosima-micro-xrce-dds-client
Version:        3.0.1
Release:        1%{?dist}
Summary:        eProsima's XRCE DDS client
License:        Apache-2.0
URL:            https://github.com/eProsima/Micro-XRCE-DDS-Client
Source0:        eprosima-micro-xrce-dds-client-3.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
eProsima's XRCE DDS client

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.

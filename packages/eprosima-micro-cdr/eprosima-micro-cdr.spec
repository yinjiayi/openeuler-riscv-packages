# SPDX-License-Identifier: Apache-2.0
Name:           eprosima-micro-cdr
Version:        2.0.2
Release:        1%{?dist}
Summary:        eProsima's Micro-CDR for serialization and deserialization
License:        Apache-2.0
URL:            https://github.com/eProsima/Micro-CDR
Source0:        eprosima-micro-cdr-2.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
eProsima's Micro-CDR for serialization and deserialization

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.2-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           comms
Version:        5.2.7
Release:        1%{?dist}
Summary:        COMMS is the C++(11) headers only library, for creating communication protocols.
License:        MPL-2.0
URL:            https://github.com/commschamp/comms
Source0:        comms-5.2.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
COMMS is the C++(11) headers only library, for creating communication protocols.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.2.7-1
- Initial openEuler RISC-V package from the full package inventory.

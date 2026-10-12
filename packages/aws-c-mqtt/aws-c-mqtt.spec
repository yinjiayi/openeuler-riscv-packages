# SPDX-License-Identifier: Apache-2.0
Name:           aws-c-mqtt
Version:        0.16.0
Release:        1%{?dist}
Summary:        AWS C99 implementation of the MQTT 3.1.1 specification
License:        Apache-2.0
URL:            https://github.com/awslabs/aws-c-mqtt
Source0:        aws-c-mqtt-0.16.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
AWS C99 implementation of the MQTT 3.1.1 specification

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16.0-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           aws-c-common
Version:        0.14.4
Release:        1%{?dist}
Summary:        Core C99 package for AWS SDK for C
License:        Apache-2.0
URL:            https://github.com/awslabs/aws-c-common
Source0:        aws-c-common-0.14.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Core C99 package for AWS SDK for C

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14.4-1
- Initial openEuler RISC-V package from the full package inventory.

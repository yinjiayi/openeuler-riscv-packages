# SPDX-License-Identifier: Apache-2.0
Name:           aws-checksums
Version:        0.2.10
Release:        1%{?dist}
Summary:        Cross-Platform HW accelerated CRC32c and CRC32 with fallback to efficient SW implementations.
License:        Apache-2.0
URL:            https://github.com/awslabs/aws-checksums
Source0:        aws-checksums-0.2.10.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Cross-Platform HW accelerated CRC32c and CRC32 with fallback to efficient SW implementations.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.10-1
- Initial openEuler RISC-V package from the full package inventory.

# SPDX-License-Identifier: Apache-2.0
Name:           libad9361
Version:        0.3
Release:        1%{?dist}
Summary:        IIO AD9361 library for filter design and handling, multi-chip sync, etc.
License:        LGPL-2.1-or-later
URL:            https://github.com/analogdevicesinc/libad9361-iio
Source0:        libad9361-0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
IIO AD9361 library for filter design and handling, multi-chip sync, etc.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Initial openEuler RISC-V package from the full package inventory.

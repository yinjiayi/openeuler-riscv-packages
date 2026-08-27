# SPDX-License-Identifier: Apache-2.0
Name:           usbunker
Version:        1.0.3
Release:        1%{?dist}
Summary:        Encrypt and decrypt USB drives with AES-256-GCM
License:        MIT
URL:            https://github.com/T9Tuco/USBunker
Source0:        usbunker-1.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Encrypt and decrypt USB drives with AES-256-GCM

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.

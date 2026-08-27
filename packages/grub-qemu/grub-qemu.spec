# SPDX-License-Identifier: Apache-2.0
Name:           grub-qemu
Version:        0.1.3
Release:        1%{?dist}
Summary:        a lightweight App for Preview full GRUB
License:        GPL-3.0-or-later
URL:            https://github.com/VC365/grub-qemu
Source0:        grub-qemu-0.1.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
a lightweight App for Preview full GRUB

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Initial openEuler RISC-V package from the full package inventory.

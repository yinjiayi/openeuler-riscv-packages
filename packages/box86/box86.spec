# SPDX-License-Identifier: Apache-2.0
Name:           box86
Version:        0.3.8
Release:        1%{?dist}
Summary:        Linux Userspace x86 Emulator with a twist
License:        MIT
URL:            https://github.com/ptitSeb/box86
Source0:        box86-0.3.8.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Linux Userspace x86 Emulator with a twist

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


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.8-1
- Initial openEuler RISC-V package from the full package inventory.

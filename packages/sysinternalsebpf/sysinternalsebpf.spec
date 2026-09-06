# SPDX-License-Identifier: Apache-2.0
Name:           sysinternalsebpf
Version:        1.6.0
Release:        1%{?dist}
Summary:        Sysinternals EBPF
License:        LGPL-2.1-or-later
URL:            https://github.com/microsoft/SysinternalsEBPF
Source0:        sysinternalsebpf-1.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Sysinternals EBPF

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Initial openEuler RISC-V package from the full package inventory.

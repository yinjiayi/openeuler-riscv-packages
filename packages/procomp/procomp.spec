# SPDX-License-Identifier: Apache-2.0
Name:           procomp
Version:        0.2.0
Release:        1%{?dist}
Summary:        Small multi-target C subset compiler with Linux and Windows x86_64 backends
License:        MIT
URL:            https://github.com/yusufprompt/procomp
Source0:        procomp-0.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Small multi-target C subset compiler with Linux and Windows x86_64 backends

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.

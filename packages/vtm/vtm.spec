# SPDX-License-Identifier: Apache-2.0
Name:           vtm
Version:        2026.07.30
Release:        1%{?dist}
Summary:        Terminal multiplexer with window manager and session sharing
License:        MIT
URL:            https://github.com/directvt/vtm
Source0:        vtm-2026.07.30.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Terminal multiplexer with window manager and session sharing

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.07.30-1
- Initial openEuler RISC-V package from the full package inventory.

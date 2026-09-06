# SPDX-License-Identifier: Apache-2.0
Name:           daggy
Version:        2.2.4
Release:        1%{?dist}
Summary:        Run multiple commands on remote servers simultaneously and save output locally
License:        MIT
URL:            https://github.com/synacker/daggy
Source0:        daggy-2.2.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Run multiple commands on remote servers simultaneously and save output locally

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.4-1
- Initial openEuler RISC-V package from the full package inventory.

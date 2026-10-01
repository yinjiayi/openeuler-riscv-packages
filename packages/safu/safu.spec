# SPDX-License-Identifier: Apache-2.0
Name:           safu
Version:        0.64.4
Release:        1%{?dist}
Summary:        C to library to reduce boiler plate code when use standard c-libs
License:        MIT
URL:            https://github.com/Elektrobit/safu
Source0:        safu-0.64.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C to library to reduce boiler plate code when use standard c-libs

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.64.4-1
- Initial openEuler RISC-V package from the full package inventory.

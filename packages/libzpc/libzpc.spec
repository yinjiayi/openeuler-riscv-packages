# SPDX-License-Identifier: Apache-2.0
Name:           libzpc
Version:        1.5.0
Release:        1%{?dist}
Summary:        Open Source library for the IBM Z Protected-key crypto feature
License:        MIT
URL:            https://github.com/opencryptoki/libzpc
Source0:        libzpc-1.5.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Open Source library for the IBM Z Protected-key crypto feature

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.

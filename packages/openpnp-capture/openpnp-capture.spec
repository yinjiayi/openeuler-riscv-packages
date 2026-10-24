# SPDX-License-Identifier: Apache-2.0
Name:           openpnp-capture
Version:        0.0.30
Release:        1%{?dist}
Summary:        A cross platform video capture library with a focus on machine vision.
License:        MIT
URL:            https://github.com/openpnp/openpnp-capture
Source0:        openpnp-capture-0.0.30.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A cross platform video capture library with a focus on machine vision.

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.30-1
- Initial openEuler RISC-V package from the full package inventory.

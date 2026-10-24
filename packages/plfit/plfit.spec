# SPDX-License-Identifier: Apache-2.0
Name:           plfit
Version:        1.0.1
Release:        1%{?dist}
Summary:        Fitting power-law distributions to empirical data
License:        GPL-2.0-or-later
URL:            https://github.com/ntamas/plfit
Source0:        plfit-1.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Fitting power-law distributions to empirical data

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
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.

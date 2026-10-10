# SPDX-License-Identifier: Apache-2.0
Name:           qmicroz
Version:        0.6
Release:        1%{?dist}
Summary:        Minimalist Zip/Unzip library. C++/Qt wrapper over miniz.
License:        MIT
URL:            https://github.com/artemvlas/qmicroz
Source0:        qmicroz-0.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Minimalist Zip/Unzip library. C++/Qt wrapper over miniz.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6-1
- Initial openEuler RISC-V package from the full package inventory.

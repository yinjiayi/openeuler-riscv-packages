# SPDX-License-Identifier: Apache-2.0
Name:           simple-password
Version:        0.1.1
Release:        3%{?dist}
Summary:        A password generator without any unnecessary stuff
License:        GPL-3.0-or-later
URL:            https://github.com/ESzPa/spass
Source0:        simple-password-0.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  vim-common

%description
A password generator without any unnecessary stuff

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
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-3
- Configure the explicit CMake source and out-of-source build directories.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-2
- Add the vim-common provider for the xxd source-generation command.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.

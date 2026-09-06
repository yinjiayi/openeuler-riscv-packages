# SPDX-License-Identifier: Apache-2.0
Name:           bdf2sfd
Version:        1.2.0
Release:        1%{?dist}
Summary:        BDF to SFD converter, allowing to vectorize bitmap fonts
License:        BSD-2-Clause
URL:            https://github.com/fcambus/bdf2sfd
Source0:        bdf2sfd-1.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
BDF to SFD converter, allowing to vectorize bitmap fonts

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.

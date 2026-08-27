# SPDX-License-Identifier: Apache-2.0
Name:           tcplay
Version:        3.3
Release:        1%{?dist}
Summary:        Free and simple TrueCrypt implementation based on dm-crypt
License:        BSD-2-Clause
URL:            https://github.com/bwalex/tc-play
Source0:        tcplay-3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libgcrypt-devel
BuildRequires:  lvm2-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  uuid-devel

%description
Free and simple TrueCrypt implementation based on dm-crypt

%prep
%autosetup -n tc-play-%{version} -p1

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
%doc README.md
%doc CHANGELOG

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package from the full package inventory.

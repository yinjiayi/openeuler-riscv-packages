# SPDX-License-Identifier: Apache-2.0
Name:           libva-intel-driver
Version:        2.4.5
Release:        1%{?dist}
Summary:        VA-API implementation for Intel G45 and HD Graphics family
License:        MIT
URL:            https://github.com/irql-notlessorequal/intel-vaapi-driver
Source0:        libva-intel-driver-2.4.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
VA-API implementation for Intel G45 and HD Graphics family

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.5-1
- Initial openEuler RISC-V package from the full package inventory.

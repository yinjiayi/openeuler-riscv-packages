# SPDX-License-Identifier: Apache-2.0
Name:           rogauracore
Version:        1.6.2
Release:        1%{?dist}
Summary:        RGB keyboard control for Asus ROG laptops
License:        MIT
URL:            https://github.com/Syndelis/rogauracore
Source0:        rogauracore-1.6.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
RGB keyboard control for Asus ROG laptops

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-1
- Initial openEuler RISC-V package from the full package inventory.

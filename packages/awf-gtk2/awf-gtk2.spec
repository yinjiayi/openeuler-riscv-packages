# SPDX-License-Identifier: Apache-2.0
Name:           awf-gtk2
Version:        4.2.0
Release:        1%{?dist}
Summary:        Theme preview application for GTK 2
License:        GPL-3.0-or-later
URL:            https://github.com/luigifab/awf-extended
Source0:        awf-gtk2-4.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Theme preview application for GTK 2

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.0-1
- Initial openEuler RISC-V package from the full package inventory.

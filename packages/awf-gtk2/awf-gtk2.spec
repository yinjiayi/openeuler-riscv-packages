# SPDX-License-Identifier: Apache-2.0
Name:           awf-gtk2
Version:        4.2.0
Release:        2%{?dist}
Summary:        Theme preview application for GTK 2
License:        GPL-3.0-or-later
URL:            https://github.com/luigifab/awf-extended
Source0:        awf-gtk2-4.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gtk2-devel
BuildRequires:  libtool
BuildRequires:  libnotify-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Theme preview application for GTK 2

%prep
%autosetup -p1 -n awf-extended-%{version}

%build
autoreconf -fi
%configure --enable-only-gtk2
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.0-2
- Match the upstream archive root and configure the GTK 2 variant with its direct build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.0-1
- Initial openEuler RISC-V package from the full package inventory.

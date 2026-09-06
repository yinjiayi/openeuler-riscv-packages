# SPDX-License-Identifier: Apache-2.0
Name:           zile
Version:        2.6.4
Release:        1%{?dist}
Summary:        A small, fast, and powerful Emacs clone
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/zile/
Source0:        zile-2.6.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gc-devel
BuildRequires:  ncurses-devel
BuildRequires:  glib2-devel
BuildRequires:  libgee-devel
BuildRequires:  vala


%description
A small, fast, and powerful Emacs clone

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.4-1
- Initial openEuler RISC-V package from the full package inventory.

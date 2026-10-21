# SPDX-License-Identifier: Apache-2.0
Name:           cppi
Version:        1.18
Release:        1%{?dist}
Summary:        C preprocessor directive indenter
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/cppi/
Source0:        cppi-1.18.tar.xz
BuildRequires:  gcc
BuildRequires:  make


%description
C preprocessor directive indenter

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_mandir}/man1/cppi.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.18-1
- Initial openEuler RISC-V package from the full package inventory.

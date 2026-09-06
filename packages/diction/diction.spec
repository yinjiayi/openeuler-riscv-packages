# SPDX-License-Identifier: Apache-2.0
Name:           diction
Version:        1.11
Release:        1%{?dist}
Summary:        Identifies diction and style errors
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/diction/
Source0:        diction-1.11.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  flex


%description
Identifies diction and style errors

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
%doc NEWS
%doc README
%{_bindir}/*
%{_datadir}/diction/
%{_mandir}/man1/diction.1*
%{_mandir}/man1/style.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11-1
- Initial openEuler RISC-V package from the full package inventory.

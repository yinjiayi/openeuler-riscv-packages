# SPDX-License-Identifier: Apache-2.0
Name:           unrtf
Version:        0.21.10
Release:        1%{?dist}
Summary:        Command-line program which converts RTF documents to other formats
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/unrtf/
Source0:        unrtf-0.21.10.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Command-line program which converts RTF documents to other formats

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
%{_datadir}/unrtf/
%{_mandir}/man1/unrtf.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21.10-1
- Initial openEuler RISC-V package from the full package inventory.

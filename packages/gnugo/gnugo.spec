# SPDX-License-Identifier: Apache-2.0
Name:           gnugo
Version:        3.8
Release:        1%{?dist}
Summary:        Program that plays the game of Go
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnugo/
Source0:        gnugo-3.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Program that plays the game of Go

%prep
%autosetup -p1
# GCC 14 rejects upstream strings passed directly as printf formats.
sed -i 's/fprintf(f, line);/fprintf(f, "%s", line);/g' engine/dfa.c
sed -i 's/sprintf(code_pos, autohelper_functions\[funcno\].code);/sprintf(code_pos, "%s", autohelper_functions[funcno].code);/' patterns/mkpat.c

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_infodir}/gnugo.info*
%{_mandir}/man6/gnugo.6*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8-1
- Initial openEuler RISC-V package from the full package inventory.

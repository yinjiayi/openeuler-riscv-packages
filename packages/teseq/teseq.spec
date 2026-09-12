# SPDX-License-Identifier: Apache-2.0
Name:           teseq
Version:        1.1.1
Release:        1%{?dist}
Summary:        A tool for control characters and terminal control sequences
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/teseq/
Source0:        teseq-1.1.1.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl


%description
A tool for control characters and terminal control sequences

%prep
%autosetup -p1

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
%{_infodir}/teseq.info*
%{_mandir}/man1/reseq.1*
%{_mandir}/man1/teseq.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Initial openEuler RISC-V package from the full package inventory.

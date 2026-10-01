# SPDX-License-Identifier: Apache-2.0
Name:           cpio
Version:        2.15
Release:        1%{?dist}
Summary:        A tool to copy files into or out of a cpio or tar archive
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/cpio/
Source0:        cpio-2.15.tar.bz2
BuildRequires:  gcc
BuildRequires:  make


%description
A tool to copy files into or out of a cpio or tar archive

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
%find_lang %{name}
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_libexecdir}/rmt
%{_infodir}/cpio.info*
%{_mandir}/man1/cpio.1*
%{_mandir}/man8/rmt.8*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.15-1
- Initial openEuler RISC-V package from the full package inventory.

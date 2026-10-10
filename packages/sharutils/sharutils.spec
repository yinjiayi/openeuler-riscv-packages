# SPDX-License-Identifier: Apache-2.0
Name:           sharutils
Version:        4.15.2
Release:        1%{?dist}
Summary:        Makes so-called shell archives out of many files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/sharutils/
Source0:        sharutils-4.15.2.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
Makes so-called shell archives out of many files

%prep
%autosetup -p1
# Teach the bundled old gnulib implementation to recognize modern glibc.
sed -i 's/^#if defined _IO_ftrylockfile || __GNU_LIBRARY__ == 1/#if defined _IO_ftrylockfile || defined __GLIBC__ || __GNU_LIBRARY__ == 1/' lib/fseeko.c

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
%{_infodir}/sharutils.info*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.15.2-1
- Initial openEuler RISC-V package from the full package inventory.

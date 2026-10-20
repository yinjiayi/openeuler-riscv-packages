# SPDX-License-Identifier: Apache-2.0
Name:           global
Version:        6.7
Release:        1%{?dist}
Summary:        Source code tagging system
License:        GPL-3.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause AND MIT AND LicenseRef-Fedora-Public-Domain AND blessing AND GFDL-1.2-or-later
URL:            https://www.gnu.org/software/global/
Source0:        global-6.7.tar.gz

# The release archive ships global.info newer than global.texi; texinfo is
# only needed when regenerating the release files.
BuildRequires:  ctags
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  python3
BuildRequires:  sqlite-devel
Requires:       ctags
Requires:       python3

%description
GNU GLOBAL indexes source trees and provides command-line and HTML navigation.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --with-included-ltdl --with-sqlite3 \
  --with-posix-sort=/usr/bin/sort --with-exuberant-ctags=/usr/bin/ctags \
  --with-python-interpreter=/usr/bin/python3
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -type f -name '*.la' -delete

%check
%make_build check

%files
%license COPYING COPYING.LIB LICENSE
%doc AUTHORS ChangeLog DONORS FAQ NEWS README THANKS
%{_bindir}/global
%{_bindir}/globash
%{_bindir}/gozilla
%{_bindir}/gtags
%{_bindir}/gtags-cscope
%{_bindir}/htags
%{_bindir}/htags-server
%{_datadir}/gtags/
%{_libdir}/gtags/
%{_infodir}/global.info*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.15-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.

# SPDX-License-Identifier: Apache-2.0
Name:           nano
Version:        9.2
Release:        1%{?dist}
Summary:        Small and friendly text editor
License:        GPL-3.0-or-later
URL:            https://nano-editor.org
Source0:        nano-9.2.tar.xz
BuildRequires:  gcc
BuildRequires:  file-devel
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  texinfo

%description
Small and friendly text editor

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
make -j1 check

%files
%license COPYING
%doc README*
%doc %{_docdir}/%{name}/*.html
%{_bindir}/nano
%{_bindir}/rnano
%{_datadir}/info/nano.info*
%{_datadir}/locale/*/LC_MESSAGES/nano.mo
%{_datadir}/nano/
%{_mandir}/man1/nano.1*
%{_mandir}/man1/rnano.1*
%{_mandir}/man5/nanorc.5*
%{_infodir}/dir

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 9.2-1
- Package the official nano 9.2 release for openEuler RISC-V.
- Preserve the serial upstream check suite and syntax files.

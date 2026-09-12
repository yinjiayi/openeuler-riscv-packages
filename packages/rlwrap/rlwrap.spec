# SPDX-License-Identifier: Apache-2.0
Name:           rlwrap
Version:        0.48
Release:        1%{?dist}
Summary:        Readline wrapper for command-line programs
License:        GPL-2.0-or-later
URL:            https://github.com/hanslub42/rlwrap
Source0:        rlwrap-0.48.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  readline-devel

%description
rlwrap uses the GNU Readline library to add line editing, history, and
completion to interactive command-line programs.

%prep
%autosetup -p1

%build
%configure --with-libptytty=no
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS BUGS ChangeLog NEWS README.md TODO
%{_bindir}/rlwrap
%{_datadir}/rlwrap/
%{_mandir}/man1/rlwrap.1*
%{_mandir}/man3/RlwrapFilter.3pm*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.48-1
- Initial package from the official rlwrap 0.48 release archive.
- Keep the upstream make check entry point enabled in the networked target build.

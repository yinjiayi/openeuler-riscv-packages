# SPDX-License-Identifier: Apache-2.0
Name:           gnuit
Version:        4.9.5
Release:        1%{?dist}
Summary:        A set of interactive text-mode tools
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnuit/
Source0:        gnuit-4.9.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel


%description
A set of interactive text-mode tools

%prep
%autosetup -p1
# Do not pass upstream copyright text as a printf format string.
sed -i 's/printf(copyright);/printf("%s", copyright);/' src/git.c

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.9.5-1
- Initial openEuler RISC-V package from the full package inventory.

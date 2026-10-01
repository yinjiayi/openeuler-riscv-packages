# SPDX-License-Identifier: Apache-2.0
Name:           serveez
Version:        0.3.1
Release:        1%{?dist}
Summary:        server framework
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/serveez/
Source0:        serveez-0.3.1.tar.lz
BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  guile-devel


%description
server framework

%prep
%autosetup -p1

%build
%configure
# The generated Guile boot source and its consumer lack parallel ordering.
make -j1

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Initial openEuler RISC-V package from the full package inventory.

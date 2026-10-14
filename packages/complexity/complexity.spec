# SPDX-License-Identifier: Apache-2.0
Name:           complexity
Version:        1.13
Release:        1%{?dist}
Summary:        Measure complexity of C source
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/complexity/
Source0:        complexity-1.13.tar.xz
BuildRequires:  autogen-devel
BuildRequires:  autogen
BuildRequires:  gcc
BuildRequires:  make


%description
Measure complexity of C source

%prep
%autosetup -p1
# Regenerate AutoOpts sources to match the library shipped by openEuler.
(cd src && autogen opts.def)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13-1
- Initial openEuler RISC-V package from the full package inventory.

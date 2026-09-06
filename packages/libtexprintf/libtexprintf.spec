# SPDX-License-Identifier: Apache-2.0
Name:           libtexprintf
Version:        1.27
Release:        1%{?dist}
Summary:        Formatted Output with tex-like syntax support
License:        GPL-3.0-or-later
URL:            https://github.com/bartp5/libtexprintf
Source0:        libtexprintf-1.27.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Formatted Output with tex-like syntax support

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.27-1
- Initial openEuler RISC-V package from the full package inventory.

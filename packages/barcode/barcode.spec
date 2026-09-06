# SPDX-License-Identifier: Apache-2.0
Name:           barcode
Version:        0.99
Release:        1%{?dist}
Summary:        A tool to convert text strings to printed bars
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/barcode/
Source0:        barcode-0.99.tar.xz
BuildRequires:  gcc
BuildRequires:  make


%description
A tool to convert text strings to printed bars

%prep
%autosetup -p1
# GCC's format-security policy rejects using generated barcode data as a
# printf format string.  Preserve the data and pass it through %s instead.
sed -i 's/sprintf(ptr, patterns\[/sprintf(ptr, "%s", patterns[/' plessey.c

%build
%configure
%make_build CFLAGS="%{optflags} -fcommon"

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.99-1
- Initial openEuler RISC-V package from the full package inventory.

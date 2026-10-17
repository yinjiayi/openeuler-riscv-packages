# SPDX-License-Identifier: Apache-2.0
Name:           tnef
Version:        1.4.18
Release:        3%{?dist}
Summary:        Program for unpacking ms-tnef MIME attachment
License:        GPL-2.0-or-later
URL:            https://github.com/verdammelt/tnef
Source0:        tnef-1.4.18.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Program for unpacking ms-tnef MIME attachment

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install

%check
# Several command-line cases create and remove the same AUTHORS fixture.
# Keep every upstream test enabled, but serialize the shared fixture access.
make -j1 check

%files
%{_bindir}/tnef
%{_mandir}/man1/tnef.1*
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.18-3
- Match the post-compression installed manual page in the RPM file manifest.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.18-2
- Run the complete upstream test suite serially to protect shared fixtures.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.18-1
- Initial openEuler RISC-V package from the full package inventory.

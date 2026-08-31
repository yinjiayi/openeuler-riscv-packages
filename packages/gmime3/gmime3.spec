# SPDX-License-Identifier: Apache-2.0
Name:           gmime3
Version:        3.2.15
Release:        3%{?dist}
Summary:        A C/C++ MIME creation and parser library with support for S/MIME, PGP, and Unix mbox spools
License:        LGPL-2.1-or-later
URL:            https://github.com/jstedfast/gmime
Source0:        gmime-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  glib2-devel >= 2.68
BuildRequires:  gpgme-devel >= 1.6.0
BuildRequires:  libgpg-error-devel
BuildRequires:  libidn2-devel >= 2.0.0
BuildRequires:  make
BuildRequires:  zlib-devel

%description
A C/C++ MIME creation and parser library with support for S/MIME, PGP, and Unix mbox spools

%prep
%autosetup -n gmime-%{version} -p1

%build
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

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.15-3
- Build the checksum-pinned upstream release asset with its generated configure script.
- Require the development libraries used by the enabled MIME, crypto, and IDN features.

* Sun Aug 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.15-2
- Use the verified upstream archive root during source preparation.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.15-1
- Initial openEuler RISC-V package from the full package inventory.

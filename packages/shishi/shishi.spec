# SPDX-License-Identifier: Apache-2.0
Name:           shishi
Version:        1.0.3
Release:        1%{?dist}
Summary:        GNU shishi package
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/shishi/
Source0:        shishi-1.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libidn2-devel
BuildRequires:  libtasn1-devel


%description
GNU shishi package

%prep
%autosetup -p1

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.

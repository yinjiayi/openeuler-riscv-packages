# SPDX-License-Identifier: Apache-2.0
Name:           httptunnel
Version:        3.3
Release:        1%{?dist}
Summary:        Creates a bidirectional virtual data connection tunnelled in HTTP requests
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/httptunnel/
Source0:        httptunnel-3.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Creates a bidirectional virtual data connection tunnelled in HTTP requests

%prep
%autosetup -p1
# Autoconf 2.13 emitted an implicit-int compiler probe that GCC 14 rejects.
sed -i 's/^main(){return(0);}$/int main(void){return 0;}/' configure
# GCC 14 rejects the omitted declaration for time(3).
sed -i '/#include "base64.h"/i #include <time.h>' htc.c

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package from the full package inventory.

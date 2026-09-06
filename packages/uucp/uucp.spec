# SPDX-License-Identifier: Apache-2.0
Name:           uucp
Version:        1.07
Release:        1%{?dist}
Summary:        Taylor UUCP is a free implementation of UUCP and is the standard UUCP used on the GNU system
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/uucp/
Source0:        uucp-1.07.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Taylor UUCP is a free implementation of UUCP and is the standard UUCP used on the GNU system

%prep
%autosetup -p1
# Autoconf 2.13 emitted an implicit-int compiler probe that GCC 14 rejects.
sed -i 's/^main(){return(0);}$/int main(void){return 0;}/' configure

%build
# The Autoconf 2.13 probes cannot recognize modern GCC, although these three
# ANSI C language features are guaranteed by the selected compiler.
export uucp_cv_c_prototypes=yes
export uucp_cv_c_void=yes
export uucp_cv_c_unsigned_char=yes
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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Initial openEuler RISC-V package from the full package inventory.

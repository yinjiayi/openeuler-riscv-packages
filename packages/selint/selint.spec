# SPDX-License-Identifier: Apache-2.0
Name:           selint
Version:        1.5.1
Release:        4%{?dist}
Summary:        Static code analysis tool for SELinux policy source files
License:        Apache-2.0
URL:            https://github.com/SELinuxProject/selint
Source0:        selint-1.5.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  check-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  help2man
BuildRequires:  libconfuse-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  uthash-devel

%description
Static code analysis tool for SELinux policy source files

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | \
  LC_ALL=C sort | \
  grep -vFx '%{_mandir}/man1/selint.1' > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%{_mandir}/man1/selint.1*
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-4
- Track the compressed manual page with an RPM-safe glob outside the
  pre-compression dynamic file list.
- Preserve the complete 18-test upstream suite and installed functionality.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-3
- Allow the audited RISC-V dependency closure enough time to install under QEMU.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-2
- Declare the complete Autotools, parser, library, header, manual, and test dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.

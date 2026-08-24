# SPDX-License-Identifier: Apache-2.0
Name:           autoconf-archive
Version:        2024.10.16
Release:        1%{?dist}
Summary:        Collection of reusable Autoconf macros
License:        GPL-2.0-or-later WITH Autoconf-exception-macro AND GPL-3.0-or-later AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GPL-3.0-or-later WITH Autoconf-exception-macro AND GFDL-1.3-or-later AND LGPL-3.0-or-later WITH Autoconf-exception-macro AND LGPL-2.1-or-later AND BSD-2-Clause AND BSD-3-Clause AND FSFAP AND FSFAP-no-warranty-disclaimer AND FSFULLR
URL:            https://www.gnu.org/software/autoconf-archive/
Source0:        autoconf-archive-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  texinfo
Requires:       autoconf
Requires:       automake

%description
GNU Autoconf Archive is a collection of more than 500 reusable Autoconf macros.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_docdir}/%{name}/COPYING*
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check
mkdir macro-smoke
cat > macro-smoke/configure.ac <<'EOF'
AC_INIT([archive-smoke], [1.0])
AC_CONFIG_SRCDIR([configure.ac])
m4_include([../m4/ax_check_compile_flag.m4])
AX_CHECK_COMPILE_FLAG([-Wall], [ax_has_wall=yes], [ax_has_wall=no])
AS_IF([test "x$ax_has_wall" != xyes],
      [AC_MSG_ERROR([compiler rejected -Wall])])
AC_OUTPUT
EOF
(cd macro-smoke && autoconf && ./configure)

%files
%license COPYING COPYING.EXCEPTION
%doc AUTHORS NEWS README
%{_datadir}/aclocal/*.m4
%{_infodir}/autoconf-archive.info*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2024.10.16-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.

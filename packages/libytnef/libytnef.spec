# SPDX-License-Identifier: Apache-2.0
Name:           libytnef
Version:        2.1.2
Release:        1%{?dist}
Summary:        Library for reading Microsoft TNEF streams
License:        GPL-2.0-or-later
URL:            https://github.com/Yeraze/ytnef
Source0:        ytnef-v%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libytnef reads Transport Neutral Encapsulation Format (TNEF) streams,
including Microsoft Outlook winmail.dat attachments.

%package devel
Summary:        Development files for libytnef
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, pkg-config metadata, and shared-library linker name for
TNEF-reading applications.

%package tools
Summary:        Command-line TNEF extraction and inspection tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl(MIME::Parser)
Requires:       perl(Mail::Mailer)

%description tools
ytnef and ytnefprint extract and inspect TNEF streams. The optional
ytnefprocess Perl helper processes TNEF parts in incoming mail.

%prep
%autosetup -n ytnef-%{version} -p1

%build
mkdir -p m4
autoreconf -vfi
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libytnef.la

%check
%make_build check
# Upstream runs its full fixture regression script in CI but does not
# register it in Automake TESTS. Keep its attachment and field assertions.
rm -rf -- test-data/data
(
  cd test-data
  bash ./test.sh
)

%files
%license COPYING
%doc ChangeLog README.md
%{_libdir}/libytnef.so.*

%files devel
%license COPYING
%{_includedir}/ytnef.h
%{_includedir}/mapi.h
%{_includedir}/mapidefs.h
%{_includedir}/mapitags.h
%{_includedir}/tnef-types.h
%{_includedir}/tnef-errors.h
%{_libdir}/libytnef.so
%{_libdir}/pkgconfig/libytnef.pc

%files tools
%license COPYING
%{_bindir}/ytnef
%{_bindir}/ytnefprint
%{_bindir}/ytnefprocess

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Package the official 2.1.2 tag and full TNEF regression suite.

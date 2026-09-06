# SPDX-License-Identifier: Apache-2.0
Name:           cppcheck
Version:        2.21.1
Release:        1%{?dist}
Summary:        Static analysis tool for C and C++ code
License:        GPL-3.0-or-later
URL:            https://cppcheck.sourceforge.io/
Source0:        cppcheck-%{version}.tar.gz

BuildRequires:  docbook-style-xsl
BuildRequires:  gcc-c++
BuildRequires:  libxml2
BuildRequires:  make
BuildRequires:  pcre-devel
BuildRequires:  pkgconf
BuildRequires:  python3
Requires:       python3
Requires:       python3-pygments

%description
Cppcheck is a static analysis tool for C and C++ code. It detects classes of
bugs that compilers commonly do not report while supporting non-standard code
and multiple target platforms.

%prep
%autosetup -p1

%build
%make_build \
  HAVE_RULES=yes \
  MATCHCOMPILER=yes \
  FILESDIR=%{_datadir}/cppcheck \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags}"
%make_build man

%install
%make_install \
  HAVE_RULES=yes \
  MATCHCOMPILER=yes \
  PREFIX=%{_prefix} \
  FILESDIR=%{_datadir}/cppcheck
install -Dpm 0644 cppcheck.1 %{buildroot}%{_mandir}/man1/cppcheck.1

%check
%make_build \
  HAVE_RULES=yes \
  MATCHCOMPILER=yes \
  FILESDIR=%{_datadir}/cppcheck \
  test checkcfg validatePlatforms checkCWEEntries validateXML

%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/cppcheck
%{_bindir}/cppcheck-htmlreport
%{_datadir}/cppcheck/
%{_mandir}/man1/cppcheck.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.21.1-1
- Initial openEuler RISC-V Cppcheck package with complete upstream tests.

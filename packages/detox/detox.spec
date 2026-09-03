# SPDX-License-Identifier: Apache-2.0

Name:           detox
Version:        3.0.1
Release:        1%{?dist}
Summary:        Utility for cleaning problematic filenames
License:        BSD-3-Clause
URL:            https://github.com/dharple/detox
Source0:        detox-%{version}.tar.gz
Patch0:         0001-tests-skip-known-unusable-valgrind-runtime.patch

BuildRequires:  bash
BuildRequires:  check-devel
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-locale-archive
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
BuildRequires:  valgrind

%description
detox replaces awkward characters in filenames with safe equivalents and
provides configurable ISO-8859-1, CP-1252, UTF-8, and CGI-unescape filters.

%prep
%autosetup -p1

%build
%configure --with-check
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/detox

%check
%make_build check

%files
%license LICENSE
%doc BUILD.md CHANGELOG.md README.md THANKS.md
%config(noreplace) %{_sysconfdir}/detoxrc
%{_bindir}/detox
%{_bindir}/inline-detox
%{_datadir}/detox/
%{_mandir}/man1/detox.1*
%{_mandir}/man1/inline-detox.1*
%{_mandir}/man5/detox.tbl.5*
%{_mandir}/man5/detoxrc.5*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package with all 17 legacy and 14 Check tests.
- Fail closed on unexpected Valgrind errors and skip its known unsupported target-runtime startup case.

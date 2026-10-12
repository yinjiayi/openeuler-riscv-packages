# SPDX-License-Identifier: Apache-2.0
Name:           unifdef
Version:        2.12
Release:        1%{?dist}
Summary:        Selectively remove C preprocessor conditionals
License:        BSD-2-Clause AND BSD-3-Clause
URL:            https://dotat.at/prog/unifdef/
Source0:        unifdef-%{version}.tar.xz

Requires:       coreutils
Requires:       gcc
Requires:       sed
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed

%description
Unifdef processes C and C++ preprocessor conditionals. Given definitions for
selected symbols, it removes directives and branches whose outcomes can be
determined while leaving unknown conditionals intact. The package also ships
unifdefall, which resolves all conditionals using the system C preprocessor.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build prefix=%{_prefix}

%install
%make_install prefix=%{_prefix}

%check
# Run every upstream shell regression and byte-for-byte expected result.
%make_build test

%files
%license COPYING
%doc Changelog README unifdef.txt
%{_bindir}/unifdef
%{_bindir}/unifdefall
%{_mandir}/man1/unifdef.1*
%{_mandir}/man1/unifdefall.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12-1
- Initial openEuler RISC-V package with the complete upstream regression suite.

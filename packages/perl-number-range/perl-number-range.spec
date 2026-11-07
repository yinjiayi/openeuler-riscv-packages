# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-number-range
Version:        0.12
Release:        1%{?dist}
Summary:        Perl numeric range membership and manipulation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Number-Range
Source0:        Number-Range-0.12.tar.gz
Patch0:         0001-check-all-scalar-values.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-Carp perl-Exporter

%description
Number::Range describes, tests and manipulates numeric ranges. It supports
individual membership queries and scalar all-of or list-context queries.

%prep
%setup -q -n Number-Range-%{version}
# Only normalize this text module's CRLF line endings before the strict LF patch.
%{__perl} -pi -e 's/\r\n/\n/g' lib/Number/Range.pm
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
# Preserve the original 40 assertions and include the new default regression.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Number/Range.pm
%{_mandir}/man3/Number::Range.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Retain upstream default tests and fix scalar multi-value membership.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-number-misc
Version:        1.2
Release:        1%{?dist}
Summary:        Perl utilities for number formatting and classification
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Number-Misc
Source0:        Number-Misc-1.2.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators


%description
Number::Misc provides utilities for interpreting and formatting numbers,
zero padding, random integers in a range, and even/odd classification.

%prep
%autosetup -n Number-Misc-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Number/Misc.pm
%{perl_vendorlib}/Number/Misc.pod
%{_mandir}/man3/Number::Misc.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Package the official release with its complete default test suite.

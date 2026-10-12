# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Symbolic
Version:        0.613
Release:        1%{?dist}
Summary:        Symbolic mathematics for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Symbolic
Source0:        Math-Symbolic-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Memoize)
BuildRequires:  perl(Parse::RecDescent)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(Memoize)
Requires:       perl(Parse::RecDescent)
Requires:       perl(Test::More)

%description
Math::Symbolic builds, parses and evaluates symbolic mathematical
expressions, with the original and bundled standalone Yapp parsers.

%prep
%autosetup -n Math-Symbolic-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every unchanged upstream default t/ file.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Symbolic.pm
%{perl_vendorlib}/Math/Symbolic/
%{perl_vendorlib}/Math/compile_yapp_parser.pl
%{_mandir}/man3/Math::Symbolic*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.613-1
- Package the official CPAN release with its complete default test suite.

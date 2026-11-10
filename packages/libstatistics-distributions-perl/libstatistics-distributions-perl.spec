# SPDX-License-Identifier: Apache-2.0
Name:           libstatistics-distributions-perl
Version:        1.02
Release:        1%{?dist}
Summary:        Calculate probabilities and quantiles for common statistical distributions in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Statistics-Distributions
Source0:        Statistics-Distributions-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Test-Harness
BuildRequires:  perl(Exporter)
BuildRequires:  perl(constant)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(constant)

%description
Calculate probabilities and quantiles for the normal, chi-square, Student's
t, and F distributions in Perl.

%prep
%setup -q -n Statistics-Distributions-%{version}
%{__perl} -0777 -ne 'if (/^=head1 COPYRIGHT[ \t]*\r?\n(.*?)^=head1 SEE ALSO/ms) { print $1 } else { die "Missing upstream copyright notice\n" }' Distributions.pm > LICENSE.upstream
test -s LICENSE.upstream

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test
prove -Iblib/lib -Iblib/arch ./test.pl

%files
%license LICENSE.upstream
%doc Changes
%{perl_vendorlib}/Statistics/Distributions.pm
%dir %{perl_vendorlib}/auto/Statistics/Distributions
%{perl_vendorlib}/auto/Statistics/Distributions/autosplit.ix
%{_mandir}/man3/Statistics::Distributions.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package the pinned source, original TAP tests and generated autosplit index.

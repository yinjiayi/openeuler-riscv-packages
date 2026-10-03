# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-AutoloadCAN
Version:        0.03
Release:        2%{?dist}
Summary:        Cooperate between Perl AUTOLOAD, can and inheritance
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-AutoloadCAN
Source0:        Class-AutoloadCAN-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators

%description
Class::AutoloadCAN implements dynamic methods through CAN callbacks, allowing
AUTOLOAD dispatch, UNIVERSAL::can and multiple inheritance to cooperate.

%prep
%autosetup -n Class-AutoloadCAN-%{version} -p1

%build
# Upstream's traditional Makefile.PL intentionally needs no Module::Build.
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the entire default test.pl and its twenty assertions.
%make_build test
# Legacy test.pl only prints failing TAP; enforce TAP failure as nonzero too.
PERL5LIB="$PWD/blib/lib:$PWD/blib/arch" %{__perl} -MTest::Harness -e 'runtests("test.pl")'

%files
%license lib/Class/AutoloadCAN.pm
%doc README Changes
%{perl_vendorlib}/Class/AutoloadCAN.pm
%{_mandir}/man3/Class::AutoloadCAN.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-2
- Enforce unchanged legacy TAP test failures through Test::Harness.
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN source with the unchanged complete upstream test.

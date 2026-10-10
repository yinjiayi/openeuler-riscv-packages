# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-CheckDeps
Version:        0.010
Release:        1%{?dist}
Summary:        Check Perl distribution dependencies in tests
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-CheckDeps
Source0:        Test-CheckDeps-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.30
BuildRequires:  perl(CPAN::Meta) >= 2.120920
BuildRequires:  perl(CPAN::Meta::Check) >= 0.007
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl-generators
Requires:       perl(CPAN::Meta) >= 2.120920
Requires:       perl(CPAN::Meta::Check) >= 0.007
Requires:       perl(Exporter) >= 5.57
Requires:       perl(List::Util)
Requires:       perl(Test::Builder)

%description
Test::CheckDeps checks the dependency requirements declared in CPAN metadata
from within a Perl test suite.

%prep
%autosetup -n Test-CheckDeps-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four original default files; upstream release-only POD checks
# self-skip unless RELEASE_TESTING is explicitly set.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/CheckDeps.pm
%{_mandir}/man3/Test::CheckDeps.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.010-1
- Package official CPAN release with its unmodified default tests.

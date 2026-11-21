# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-cpan-meta-json
Version:        0.16
Release:        1%{?dist}
Summary:        Validate CPAN META.json files
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Test-CPAN-Meta-JSON
Source0:        Test-CPAN-Meta-JSON-0.16.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(JSON) >= 2.15
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More) >= 0.70
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(IO::File)
Requires:       perl(JSON) >= 2.15
Requires:       perl(Test::Builder)
Requires:       perl(strict)
Requires:       perl(vars)
Requires:       perl(warnings)

%description
Validate CPAN META.json files

%prep
%autosetup -n Test-CPAN-Meta-JSON-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Test/CPAN/Meta/JSON.pm
%{perl_vendorlib}/Test/CPAN/Meta/JSON/Version.pm
%{_mandir}/man3/Test::CPAN::Meta::JSON.3*
%{_mandir}/man3/Test::CPAN::Meta::JSON::Version.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16-1
- Package the fixed CPAN release and retain the original default tests.

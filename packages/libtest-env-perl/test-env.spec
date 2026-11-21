# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-env
Version:        1.088
Release:        1%{?dist}
Summary:        Test values of environment variables
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Test-Env
Source0:        Test-Env-1.088.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.8.0
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.86
BuildRequires:  perl-generators
Requires:       perl >= 5.8.0
Requires:       perl(Exporter)
Requires:       perl(Test::Builder)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Test values of environment variables

%prep
%autosetup -n Test-Env-%{version} -p1

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
%doc Changes README.pod SECURITY.md
%{perl_vendorlib}/Test/Env.pm
%{_mandir}/man3/Test::Env.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.088-1
- Package the fixed CPAN release and retain the original default tests.

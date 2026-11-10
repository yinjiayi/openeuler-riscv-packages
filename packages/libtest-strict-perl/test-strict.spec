# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-strict
Version:        0.54
Release:        1%{?dist}
Summary:        Test Perl syntax and strict-mode declarations
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Test-Strict
Source0:        Test-Strict-0.54.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6.0
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Find) >= 0.01
BuildRequires:  perl(File::Spec) >= 0.01
BuildRequires:  perl(File::Temp) >= 0.01
BuildRequires:  perl(FindBin) >= 0.01
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(Test::Builder) >= 0.01
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::More) >= 1.00
BuildRequires:  perl(Test::Pod) >= 1.48
BuildRequires:  perl(Test::Pod::Coverage) >= 1.10
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl >= 5.6.0
Requires:       perl(Config)
Requires:       perl(File::Find) >= 0.01
Requires:       perl(File::Spec) >= 0.01
Requires:       perl(File::Temp) >= 0.01
Requires:       perl(FindBin) >= 0.01
Requires:       perl(Test::Builder) >= 0.01
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test Perl syntax and strict-mode declarations

%prep
%autosetup -n Test-Strict-%{version} -p1

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
%{perl_vendorlib}/Test/Strict.pm
%{_mandir}/man3/Test::Strict.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.54-1
- Package the fixed CPAN release and retain the original default tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-eol
Version:        2.02
Release:        1%{?dist}
Summary:        Check line endings in Perl projects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-EOL
Source0:        Test-EOL-2.02.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Cwd)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(Test::Builder)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::EOL detects incorrect line endings and optionally checks for trailing
whitespace in Perl projects.

%prep
%autosetup -n Test-EOL-%{version} -p1

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
%license LICENCE
%doc Changes README
%{perl_vendorlib}/Test/EOL.pm
%{_mandir}/man3/Test::EOL.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.02-1
- Package the fixed CPAN release and retain the original default tests.

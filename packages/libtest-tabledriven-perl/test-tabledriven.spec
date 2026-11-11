# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-tabledriven
Version:        0.02
Release:        1%{?dist}
Summary:        Write table-driven Perl tests with minimal boilerplate
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-TableDriven
Source0:        Test-TableDriven-0.02.tar.gz
Source1:        Module-Install-0.67-README
Source2:        Module-Install-0.67-LICENSE
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Data::Dumper)
Requires:       perl(Test::More)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Write table-driven Perl tests with minimal boilerplate

%prep
%autosetup -n Test-TableDriven-%{version} -p1
cp -p %{SOURCE1} MODULE-INSTALL-NOTICE
cp -p %{SOURCE2} MODULE-INSTALL-LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license lib/Test/TableDriven.pm
%license MODULE-INSTALL-NOTICE MODULE-INSTALL-LICENSE
%doc README Changes
%{perl_vendorlib}/Test/TableDriven.pm
%{_mandir}/man3/Test::TableDriven.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package the fixed official source with its unchanged default test suite.

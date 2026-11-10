# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-sub
Version:        1.001
Release:        1%{?dist}
Summary:        Tie Perl hash fetches to a subroutine
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Tie-Sub
Source0:        Tie-Sub-1.001.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl >= 5.006
BuildRequires:  perl(Carp)
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(English)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Differences) >= 0.60
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl >= 5.006
Requires:       perl(Carp)
Requires:       perl(Params::Validate)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Tie Perl hash fetches to a subroutine

%prep
%autosetup -n Tie-Sub-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

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
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Tie/Sub.pm
%{_mandir}/man3/Tie::Sub.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.001-1
- Package the fixed CPAN release and retain the original default tests.

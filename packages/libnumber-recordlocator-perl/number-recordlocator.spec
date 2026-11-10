# SPDX-License-Identifier: Apache-2.0
Name:           perl-number-recordlocator
Version:        0.005
Release:        1%{?dist}
Summary:        Encode numbers as human-readable record locators
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Number-RecordLocator
Source0:        Number-RecordLocator-0.005.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(vars)
BuildRequires:  perl(Carp)
BuildRequires:  perl(bigint)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(vars)
Requires:       perl(Carp)
Requires:       perl(bigint)

%description
Encode numbers as human-readable record locators

%prep
%autosetup -n Number-RecordLocator-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
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
%{perl_vendorlib}/Number/RecordLocator.pm
%{_mandir}/man3/Number::RecordLocator.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.005-1
- Package the verified CPAN release and retain all four upstream tests.

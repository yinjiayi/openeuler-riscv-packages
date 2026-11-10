# SPDX-License-Identifier: Apache-2.0
Name:           perl-devel-strictmode
Version:        0.003
Release:        1%{?dist}
Summary:        Perl constants for enabling strict runtime checks
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Devel-StrictMode
Source0:        Devel-StrictMode-0.003.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl-generators
BuildRequires:  make
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Devel::StrictMode exports a Perl constant for enabling strict runtime checks
in test environments and optionally exports the opposite value.

%prep
%autosetup -n Devel-StrictMode-%{version} -p1

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
%license LICENSE COPYRIGHT
%doc README Changes
%{perl_vendorlib}/Devel/StrictMode.pm
%{_mandir}/man3/Devel::StrictMode.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003-1
- Package the verified CPAN release and retain both default tests.

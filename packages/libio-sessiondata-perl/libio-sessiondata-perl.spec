# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-SessionData
Version:        1.03
Release:        1%{?dist}
Summary:        Perl session data and session set classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IO-SessionData
Source0:        IO-SessionData-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
IO::SessionData and IO::SessionSet provide session support classes
distributed separately from SOAP::Lite.

%prep
%autosetup -n IO-SessionData-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/IO/SessionData.pm
%{perl_vendorlib}/IO/SessionSet.pm

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official CPAN release with original tests.

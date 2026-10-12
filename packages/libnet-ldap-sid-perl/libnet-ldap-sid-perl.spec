# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-LDAP-SID
Version:        0.001
Release:        1%{?dist}
Summary:        LDAP security identifier conversion for Perl
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Net-LDAP-SID
Source0:        Net-LDAP-SID-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Carp)

%description
Net::LDAP::SID converts Windows/LDAP security identifiers between their
textual and binary representations.

%prep
%autosetup -n Net-LDAP-SID-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both functional tests and the three upstream author-only test files.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Net/LDAP/SID.pm
%{_mandir}/man3/Net::LDAP::SID.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.001-1
- Package official CPAN release with all original default test files.

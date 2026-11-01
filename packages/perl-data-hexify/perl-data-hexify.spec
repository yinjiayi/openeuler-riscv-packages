# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Hexify
Version:        1.00
Release:        1%{?dist}
Summary:        Perl hexadecimal dump of arbitrary data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Hexify
Source0:        Data-Hexify-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Data::Hexify formats arbitrary data as configurable hexadecimal dumps.

%prep
%autosetup -n Data-Hexify-%{version} -p1

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
%{perl_vendorlib}/Data/Hexify.pm
%{_mandir}/man3/Data::Hexify.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package official CPAN release with original tests.

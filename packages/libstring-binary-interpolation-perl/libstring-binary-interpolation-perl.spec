# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Binary-Interpolation
Version:        1.0.1
Release:        1%{?dist}
Summary:        Interpolate byte values written as binary digits in Perl strings
License:        GPL-2.0-only OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Binary-Interpolation
Source0:        String-Binary-Interpolation-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Binary::Interpolation defines Perl variables for all byte values,
allowing individual bytes to be written as binary digits in interpolated
strings.

%prep
%autosetup -n String-Binary-Interpolation-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three upstream default tests; both POD dependencies are required.
%make_build test

%files
%license ARTISTIC.txt GPL2.txt
%doc CHANGELOG
%{perl_vendorlib}/String/Binary/Interpolation.pm
%{_mandir}/man3/String::Binary::Interpolation.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Package official CPAN release and retain all default upstream tests.

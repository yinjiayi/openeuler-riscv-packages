# SPDX-License-Identifier: Apache-2.0
Name:           perl-Statistics-Lite
Version:        3.62
Release:        1%{?dist}
Summary:        Simple functional statistics for small Perl data sets
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/Statistics-Lite
Source0:        Statistics-Lite-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Statistics::Lite provides basic statistical functions such as mean,
median, mode, variance, standard deviation and frequency counts.

%prep
%autosetup -n Statistics-Lite-%{version} -p1

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
%doc Changes
%{perl_vendorlib}/Statistics/Lite.pm
%{_mandir}/man3/Statistics::Lite.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.62-1
- Package official CPAN release with all nine original default test files.

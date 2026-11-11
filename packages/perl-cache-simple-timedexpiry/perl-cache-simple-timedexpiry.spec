# SPDX-License-Identifier: Apache-2.0
Name:           perl-Cache-Simple-TimedExpiry
Version:        0.27
Release:        1%{?dist}
Summary:        Lightweight Perl cache with timed expiration
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Cache-Simple-TimedExpiry
Source0:        Cache-Simple-TimedExpiry-0.27.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Path
BuildRequires:  perl-PathTools
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Cache::Simple::TimedExpiry implements a lightweight in-process cache with
time-based entry expiration and simple store, fetch, and key-query methods.

%prep
%autosetup -n Cache-Simple-TimedExpiry-%{version} -p1

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license META.yml Makefile.PL lib/Cache/Simple/TimedExpiry.pm
%doc Changes
%{perl_vendorlib}/Cache/Simple/TimedExpiry.pm
%{_mandir}/man3/Cache::Simple::TimedExpiry.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27-1
- Package the fixed official release and preserve the complete default tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Touch
Version:        0.12
Release:        1%{?dist}
Summary:        Update file access and modification times from Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Touch
Source0:        File-Touch-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)

%description
File::Touch updates file access and modification times and can create
missing files when requested by Perl applications.

%prep
%autosetup -n File-Touch-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both upstream default suites, including all 18 timestamp assertions.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/Touch.pm
%{_mandir}/man3/File::Touch.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Package the official stable CPAN release and both upstream test files.

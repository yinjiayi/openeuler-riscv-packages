# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Which
Version:        1.27
Release:        1%{?dist}
Summary:        Perl API for finding executable programs in search paths
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Which
Source0:        File-Which-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Env)
BuildRequires:  perl(Test::More)

%description
File::Which provides the which and where functions for locating executable
programs in the current search path.

%prep
%autosetup -n File-Which-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default upstream test files and their platform-specific
# upstream skip decisions.
%make_build test

%files
%license LICENSE
%doc Changes INSTALL README
%{perl_vendorlib}/File/Which.pm
%{_mandir}/man3/File::Which.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.27-1
- Package the official stable CPAN release and upstream tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-FnMatch
Version:        0.02
Release:        1%{?dist}
Summary:        Perl XS binding for POSIX fnmatch
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-FnMatch
Source0:        File-FnMatch-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl-generators

%description
File::FnMatch exposes the system POSIX fnmatch function and matching
flags to Perl. This package builds the architecture-specific XS module.

%prep
%autosetup -n File-FnMatch-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both upstream t files and their POSIX flag checks.
%make_build test

%files
%doc README Changes
%{perl_vendorarch}/File/FnMatch.pm
%{perl_vendorarch}/auto/File/FnMatch/FnMatch.so
%{_mandir}/man3/File::FnMatch.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN XS release with complete default tests.

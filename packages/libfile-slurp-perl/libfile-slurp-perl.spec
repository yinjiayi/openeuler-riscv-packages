# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Slurp
Version:        9999.32
Release:        1%{?dist}
Summary:        Perl routines to read, write, and edit complete files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Slurp
Source0:        File-Slurp-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Slurp provides simple routines for reading, writing, and editing
entire files and reading directory entries from Perl.

%prep
%autosetup -n File-Slurp-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all 30 upstream default test files. Their platform-specific SKIP/TODO
# branches remain upstream-controlled and are not counted as passed checks.
%make_build test

%files
%doc Changes README.md
%{perl_vendorlib}/File/Slurp.pm
%{_mandir}/man3/File::Slurp.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 9999.32-1
- Package the official CPAN release and complete default upstream tests.

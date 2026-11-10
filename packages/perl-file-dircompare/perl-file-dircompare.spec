# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-dircompare
Version:        0.7
Release:        1%{?dist}
Summary:        Compare directory trees using Perl callbacks
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-DirCompare
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAVINC/File-DirCompare-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(File::Spec)
Requires:       perl

%description
Compare directory trees, reporting changed and unique entries through
callbacks. Symbolic links are compared by their stored targets.

%prep
%setup -q -n File-DirCompare-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license README
%doc TODO
%{perl_vendorlib}/File/DirCompare.pm
%{_mandir}/man3/File::DirCompare.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7-1
- Package the fixed release and retain the complete default test suite.

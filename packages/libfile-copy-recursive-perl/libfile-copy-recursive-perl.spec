# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Copy-Recursive
Version:        0.45
Release:        1%{?dist}
Summary:        Recursive file and directory copying for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Copy-Recursive
Source0:        File-Copy-Recursive-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::File)
BuildRequires:  perl(Test::Warnings)

%description
File::Copy::Recursive copies and moves files and directory trees while
optionally preserving file modes and traversing to a selected depth.

%prep
%autosetup -n File-Copy-Recursive-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five default upstream test files. Their operating-system and
# permission-specific SKIP branches remain governed by upstream tests.
%make_build test

%files
%doc Changes README README.md
%{perl_vendorlib}/File/Copy/Recursive.pm
%{_mandir}/man3/File::Copy::Recursive.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.45-1
- Package the official CPAN release and complete default upstream tests.

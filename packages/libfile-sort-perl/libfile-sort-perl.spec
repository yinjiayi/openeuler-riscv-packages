# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Sort
Version:        1.01
Release:        1%{?dist}
Summary:        Sort files with a portable Perl API
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Sort
Source0:        File-Sort-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
File::Sort sorts files without requiring the platform's sort command or
loading the entire input into Perl memory.

%prep
%autosetup -n File-Sort-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the complete upstream test.pl, which covers eight sort assertions.
%make_build test

%files
%doc README
%{perl_vendorlib}/File/Sort.pm
%{_mandir}/man3/File::Sort.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package official CPAN release with its full upstream test.pl.

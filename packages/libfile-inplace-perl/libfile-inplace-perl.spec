# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Inplace
Version:        0.20
Release:        1%{?dist}
Summary:        Edit a file in place with optional backup
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Inplace
Source0:        File-Inplace-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Inplace edits a file through a temporary output file, with optional
backup and rollback behavior.

%prep
%autosetup -n File-Inplace-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The sole upstream test file exercises all 21 assertions in a fresh tree.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/Inplace.pm
%{_mandir}/man3/File::Inplace.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.20-1
- Package official CPAN release with the complete default upstream test.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-CountLines
Version:        0.0.3
Release:        1%{?dist}
Summary:        Perl module for counting line breaks in files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-CountLines
Source0:        File-CountLines-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)

%description
File::CountLines counts line separators in files using buffered reads,
including configurable separator styles and multi-byte separators.

%prep
%autosetup -n File-CountLines-v%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both upstream default tests and provide Test::Pod for the POD test.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/File/CountLines.pm
%{_mandir}/man3/File::CountLines.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.3-1
- Package the official stable CPAN release and unchanged upstream tests.

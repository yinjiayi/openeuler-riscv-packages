# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-LoadLines
Version:        1.047
Release:        1%{?dist}
Summary:        Perl module for loading text lines from files and data URLs
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-LoadLines
Source0:        File-LoadLines-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.76
BuildRequires:  perl-generators
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI::Escape)

%description
File::LoadLines decodes text files and data URLs into lines, including
Unicode byte-order marks and several line terminator formats.

%prep
%autosetup -n File-LoadLines-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 14 upstream default test files and their Unicode fixtures.
%make_build test

%files
%doc Changes README.md
%{perl_vendorlib}/File/LoadLines.pm
%{_mandir}/man3/File::LoadLines.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.047-1
- Package the official stable CPAN release and unchanged upstream tests.

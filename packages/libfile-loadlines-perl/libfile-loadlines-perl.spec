# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-LoadLines
Version:        1.047
Release:        1%{?dist}
Summary:        Load text lines from files with encoding detection
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-LoadLines
Source0:        File-LoadLines-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-MIME-Base64
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-URI
BuildRequires:  perl-generators

%description
File::LoadLines loads small or moderate text files into lines while
recognizing encodings, byte-order marks, and several line endings.
It also provides an optional raw-blob reader.

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
# Retain the complete 14-file default upstream suite and local fixtures.
%make_build test

%files
%doc README.md Changes
%{perl_vendorlib}/File/LoadLines.pm
%{_mandir}/man3/File::LoadLines.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.047-1
- Package official CPAN release with the complete default upstream suite.

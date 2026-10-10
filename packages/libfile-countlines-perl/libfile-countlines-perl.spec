# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-CountLines
Version:        0.0.3
Release:        1%{?dist}
Summary:        Efficiently count line breaks in a file
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-CountLines
Source0:        File-CountLines-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::CountLines counts line breaks in files, with support for common line
ending styles and custom separators.

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
# Retain both default upstream test files, including the optional POD test.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/CountLines.pm
%{_mandir}/man3/File::CountLines.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.3-1
- Package official CPAN release with both default upstream tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Grep
Version:        0.02
Release:        1%{?dist}
Summary:        Pattern matching across a series of files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Grep
Source0:        File-Grep-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Grep provides grep, map, and per-line callbacks over one or more
files or filehandles.

%prep
%autosetup -n File-Grep-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete one-file default upstream test suite.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/Grep.pm
%{_mandir}/man3/File::Grep.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with its complete default test.

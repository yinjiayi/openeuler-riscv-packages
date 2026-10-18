# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Finder
Version:        1.01
Release:        1%{?dist}
Summary:        Find-style predicate builder for Perl File::Find
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Finder
Source0:        File-Finder-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Find-Rule
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Text-Glob
BuildRequires:  perl-generators
Requires:       perl(Text::Glob)

%description
File::Finder builds File::Find predicates using find-style steps and can
return matching paths directly. This package includes its companion
File::Finder::Steps module.

%prep
%autosetup -n File-Finder-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all eight default upstream t files, including conditional tests.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/Finder.pm
%{perl_vendorlib}/File/Finder/Steps.pm
%{_mandir}/man3/File::Finder.3*
%{_mandir}/man3/File::Finder::Steps.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package official CPAN release with the complete default test pattern.

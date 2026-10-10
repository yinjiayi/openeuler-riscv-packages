# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Find-Rule-VCS
Version:        1.09
Release:        1%{?dist}
Summary:        Exclude version-control directories from File::Find::Rule searches
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Find-Rule-VCS
Source0:        File-Find-Rule-VCS-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Find-Rule >= 0.20
BuildRequires:  perl-Text-Glob >= 0.08
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Find::Rule::VCS extends File::Find::Rule with methods that exclude
version-control directories and files from a filesystem search.

%prep
%autosetup -n File-Find-Rule-VCS-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete three-file default upstream test suite.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/Find/Rule/VCS.pm
%{_mandir}/man3/File::Find::Rule::VCS.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package official CPAN release with its complete default test suite.

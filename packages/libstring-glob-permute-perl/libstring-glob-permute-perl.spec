# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Glob-Permute
Version:        0.01
Release:        1%{?dist}
Summary:        Expand glob-style string permutations without filesystem access
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Glob-Permute
Source0:        String-Glob-Permute-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Glob::Permute enumerates brace and bracket expansions from a
string pattern independently of the files present on disk.

%prep
%autosetup -n String-Glob-Permute-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete upstream default t/*.t suite (one file, 15 assertions).
%make_build test

%files
%license LICENSE.TXT
%doc README Changes
%{perl_vendorlib}/String/Glob/Permute.pm
%{_mandir}/man3/String::Glob::Permute.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package official CPAN release with all default upstream tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Trim
Version:        1.04
Release:        1%{?dist}
Summary:        Trim leading and trailing whitespace in Perl strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Trim
Source0:        Text-Trim-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Encode
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Trim provides trim, ltrim and rtrim functions for scalar and list
values, including Unicode whitespace handled by Perl regular expressions.

%prep
%autosetup -n Text-Trim-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all seven default t files, including Unicode and POD coverage.
%make_build test

%files
%license LICENSE
%doc README README.md Changes
%{perl_vendorlib}/Text/Trim.pm
%{_mandir}/man3/Text::Trim.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package official CPAN release with complete default upstream tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Typography
Version:        0.01
Release:        1%{?dist}
Summary:        Convert ASCII punctuation to HTML typography entities
License:        BSD-3-Clause
URL:            https://metacpan.org/dist/Text-Typography
Source0:        Text-Typography-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Typography converts plain ASCII punctuation into typographic HTML
entities while preserving markup within code blocks.

%prep
%autosetup -n Text-Typography-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both default upstream tests, including the POD test.
%make_build test

%files
%license lib/Text/Typography.pm
%doc README INSTALL
%{perl_vendorlib}/Text/Typography.pm
%{_mandir}/man3/Text::Typography.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package official CPAN release with both default upstream tests.

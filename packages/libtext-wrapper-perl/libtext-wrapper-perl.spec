# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Wrapper
Version:        1.05
Release:        2%{?dist}
Summary:        Wrap text by breaking long lines without changing spacing
License:        GPL-1.0-or-later OR Artistic-1.0
URL:            https://metacpan.org/dist/Text-Wrapper
Source0:        Text-Wrapper-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Differences
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Wrapper breaks long lines into shorter lines without altering existing
whitespace or combining short lines.

%prep
%autosetup -n Text-Wrapper-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream t files, including Unicode wrapping.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Wrapper.pm
%{_mandir}/man3/Text::Wrapper.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.05-2
- Correct the license identifier to the bundled generic Artistic 1.0 variant.

* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.05-1
- Package official CPAN release with full default tests and installed smoke.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Greeking
Version:        0.15
Release:        1%{?dist}
Summary:        Generate placeholder text for layout design
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Greeking
Source0:        Text-Greeking-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Greeking generates meaningless text to fill layouts during design.

%prep
%autosetup -n Text-Greeking-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three default tests and activate the upstream POD tests.
RELEASE_TESTING=1 %make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Greeking.pm
%{_mandir}/man3/Text::Greeking.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package official CPAN release with all default tests and installed smoke.

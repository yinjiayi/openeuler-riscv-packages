# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Lorem
Version:        0.34
Release:        1%{?dist}
Summary:        Generate placeholder Latin-looking text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Lorem
Source0:        Text-Lorem-%{version}.tar.gz
Patch0:         0001-cli-request-scalar-text-from-generators.patch

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Getopt::Std)

%description
Text::Lorem generates random Latin-looking words, sentences and paragraphs
for placeholder content. The package also includes its small lorem command.

%prep
%autosetup -n Text-Lorem-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
install -Dpm 0755 bin/lorem %{buildroot}%{_bindir}/lorem

%check
# Retain all five default upstream test files.
%make_build test

%files
%license README
%doc CHANGES
%{_bindir}/lorem
%{perl_vendorlib}/Text/Lorem.pm
%{_mandir}/man3/Text::Lorem.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.34-1
- Package official CPAN release with full tests, command and installed smoke.
- Request scalar text from the context-sensitive CLI generators.

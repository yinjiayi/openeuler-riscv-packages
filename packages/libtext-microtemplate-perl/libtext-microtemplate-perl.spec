# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-MicroTemplate
Version:        0.24
Release:        1%{?dist}
Summary:        Small Perl template renderer with automatic HTML escaping
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-MicroTemplate
Source0:        Text-MicroTemplate-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Temp
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::MicroTemplate renders small Perl-based templates with context-aware
HTML escaping. It also includes file-based rendering helpers.

%prep
%autosetup -n Text-MicroTemplate-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 16 unmodified default t/*.t files. IO::Scalar is required so
# the conditional warning test executes rather than skipping for absence.
%make_build test

%files
%license lib/Text/MicroTemplate.pm
%doc Changes README
%{perl_vendorlib}/Text/MicroTemplate.pm
%{perl_vendorlib}/Text/MicroTemplate/
%{_mandir}/man3/Text::MicroTemplate*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.24-1
- Package official CPAN release with complete default upstream tests.

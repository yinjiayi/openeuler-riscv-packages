# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Dumper-Concise
Version:        2.023
Release:        1%{?dist}
Summary:        Concise Perl data dumps with warning helpers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Dumper-Concise
Source0:        Data-Dumper-Concise-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Devel::ArgNames)
Requires:       perl(Devel::ArgNames)

%description
Data::Dumper::Concise provides readable Perl data dumps and warning
helpers, including named argument output through Devel::ArgNames.

%prep
%autosetup -n Data-Dumper-Concise-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain every original t/*.t file; the installed build dependency exercises DwarnN.
%{__perl} -MDevel::ArgNames -e 1
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/Dumper/Concise.pm
%{perl_vendorlib}/Data/Dumper/Concise/
%{perl_vendorlib}/Devel/Dwarn.pm
%{_mandir}/man3/Data::Dumper::Concise*.3*
%{_mandir}/man3/Devel::Dwarn.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.023-1
- Package official CPAN release with all original tests.

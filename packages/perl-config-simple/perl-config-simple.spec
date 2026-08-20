# SPDX-License-Identifier: Apache-2.0
Name:           perl-Config-Simple
Version:        4.59
Release:        1%{?dist}
Summary:        Simple Perl configuration file class
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Config-Simple
Source0:        Config-Simple-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)

%description
Config::Simple reads, writes, imports, and ties simple configuration files
using INI, simple, or HTTP-style syntax.

%prep
%autosetup -p1 -n Config-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/Config/
%{perl_vendorlib}/auto/Config/
%{_mandir}/man3/Config::Simple.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.59-1
- Initial openEuler RISC-V package with all 89 upstream tests.

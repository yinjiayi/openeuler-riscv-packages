# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-carp-assert
Version:        0.22
Release:        1%{?dist}
Summary:        Executable assertions for Perl programs
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Carp-Assert
Source0:        https://cpan.metacpan.org/authors/id/Y/YV/YVES/Carp-Assert-%{version}.tar.gz
Patch0:         patches/0001-preserve-test-helper-license.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple >= 0.88
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Carp
Requires:       perl-Exporter

%description
Carp::Assert provides executable checks for assumptions, equality and inequality,
with the original assertion-enabled and assertion-disabled modes.

%prep
%setup -q -n Carp-Assert-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license lib/Carp/Assert.pm BUILD-HELPER-LICENSE
%doc README Changes INSTALL
%{perl_vendorlib}/Carp/Assert.pm
%{_mandir}/man3/Carp::Assert.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.22-1
- Preserve original default assertions and exact embedded-test helper notices.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-AsObject
Version:        0.13
Release:        1%{?dist}
Summary:        Hashes with object-style accessors and mutators
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-AsObject
Source0:        Hash-AsObject-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(YAML)
BuildRequires:  perl-generators

%description
Hash::AsObject allows hash keys to be read and written through object-style
accessor methods while retaining normal hash-reference access.

%prep
%autosetup -n Hash-AsObject-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all ten default upstream files, including POD coverage.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Hash/AsObject.pm
%{_mandir}/man3/Hash::AsObject*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Package official CPAN release and retain the complete default upstream suite.

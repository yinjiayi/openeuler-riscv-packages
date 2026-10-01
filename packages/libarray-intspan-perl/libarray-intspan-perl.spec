# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-IntSpan
Version:        2.004
Release:        1%{?dist}
Summary:        Arrays of values indexed by integer ranges
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Array-IntSpan
Source0:        Array-IntSpan-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Array::IntSpan stores scalars or objects across compact integer ranges
and provides lookup and range-update operations.

%prep
%autosetup -n Array-IntSpan-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# All eight registered upstream t/*.t files; no test selection or skips.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Array/IntSpan.pm
%{perl_vendorlib}/Array/IntSpan/
%{_mandir}/man3/Array::IntSpan*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.004-1
- Package the official CPAN release and complete upstream test suite.

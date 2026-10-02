# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-FromHash
Version:        0.05
Release:        1%{?dist}
Summary:        Construct URI objects and strings from named fields
License:        Artistic-2.0
URL:            https://metacpan.org/dist/URI-FromHash
Source0:        URI-FromHash-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(URI) >= 1.68
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Params::Validate)
Requires:       perl(URI) >= 1.68

%description
URI::FromHash constructs URI strings or URI objects from validated named
parts, including authority, path, query and fragment values.

%prep
%autosetup -n URI-FromHash-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENSE
%doc README.md Changes INSTALL
%{perl_vendorlib}/URI/FromHash.pm
%{_mandir}/man3/URI::FromHash.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN source and preserve all default upstream tests.

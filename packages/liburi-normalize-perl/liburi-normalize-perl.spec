# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-Normalize
Version:        0.002
Release:        1%{?dist}
Summary:        Normalize URI paths in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-Normalize
Source0:        URI-Normalize-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(URI)
BuildRequires:  perl(Test::More)
Requires:       perl(Exporter)
Requires:       perl(Scalar::Util)
Requires:       perl(URI)

%description
URI::Normalize canonicalizes URI path segments, percent encoding,
scheme and host casing, and default ports.

%prep
%autosetup -n URI-Normalize-%{version} -p1

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
%doc README Changes
%{perl_vendorlib}/URI/Normalize.pm
%{_mandir}/man3/URI::Normalize.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.002-1
- Package official CPAN source and preserve all default upstream tests.

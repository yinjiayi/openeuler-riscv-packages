# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-Query
Version:        0.16
Release:        1%{?dist}
Summary:        Manipulate URI query strings in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-Query
Source0:        URI-Query-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone)
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(YAML)
Requires:       perl(Carp)
Requires:       perl(Clone)
Requires:       perl(parent)
Requires:       perl(URI::Escape)

%description
URI::Query parses, changes, and serializes URI query strings while retaining
repeated parameter values.

%prep
%autosetup -n URI-Query-%{version} -p1

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
%doc README ChangeLog TODO
%{perl_vendorlib}/URI/Query.pm
%{_mandir}/man3/URI::Query.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16-1
- Package official CPAN source and preserve all default upstream tests.

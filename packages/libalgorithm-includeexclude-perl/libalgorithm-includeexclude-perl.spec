# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-IncludeExclude
Version:        0.01
Release:        1%{?dist}
Summary:        Evaluate hierarchical include and exclude rules in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-IncludeExclude
Source0:        Algorithm-IncludeExclude-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Carp)

%description
Algorithm::IncludeExclude evaluates hierarchical path include and exclude
rules, including rules with regular-expression path components.

%prep
%autosetup -n Algorithm-IncludeExclude-%{version} -p1

%build
# The official SHA-verified archive bundles inc/Module/Install; modern Perl
# omits the current directory from @INC, so expose this source tree for only
# the Makefile.PL invocation.
PERL5LIB=. %{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Algorithm/IncludeExclude.pm
%{_mandir}/man3/Algorithm::IncludeExclude.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the official CPAN release with all default upstream tests.

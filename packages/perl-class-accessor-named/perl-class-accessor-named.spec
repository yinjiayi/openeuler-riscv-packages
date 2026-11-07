# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-accessor-named
Version:        0.009
Release:        1%{?dist}
Summary:        Give Class::Accessor generated accessors names for profiling
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Named
Source0:        https://cpan.metacpan.org/authors/id/J/JE/JESSE/Class-Accessor-Named-%{version}.tar.gz
Patch0:         patches/0001-preserve-module-install-license.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.42
BuildRequires:  perl-Class-Accessor
BuildRequires:  perl-Hook-LexWrap
BuildRequires:  perl-Sub-Name
BuildRequires:  perl-UNIVERSAL-require
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Class-Accessor
Requires:       perl-Hook-LexWrap
Requires:       perl-Sub-Name
Requires:       perl-UNIVERSAL-require

%description
This development aid names the generated accessors of Class::Accessor
and Class::Accessor::Fast so a profiler can distinguish them.

%prep
%setup -q -n Class-Accessor-Named-%{version}
%patch -P 0 -p1

%build
PERL_AUTOINSTALL=--skipdeps perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license README lib/Class/Accessor/Named.pm MODULE-INSTALL-LICENSE
%doc Changes
%{perl_vendorlib}/Class/Accessor/Named.pm
%{_mandir}/man3/Class::Accessor::Named.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.009-1
- Package the fixed upstream release with original tests and installer license notices.

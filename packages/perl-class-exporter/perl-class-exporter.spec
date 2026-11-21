# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-exporter
Version:        0.03
Release:        1%{?dist}
Summary:        Export object methods as Perl subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Exporter
Source0:        https://cpan.metacpan.org/authors/id/S/SP/SPLICE/Class-Exporter-%{version}.tar.gz
Patch0:         patches/0001-preserve-donor-licenses.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.5
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Carp
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Carp

%description
Class::Exporter exports object methods as subroutines while maintaining an
independent object instance for each importing package.

%prep
%setup -q -n Class-Exporter-%{version}
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
%license README lib/Class/Exporter.pm t/lib/Test/Builder.pm t/lib/Test/More.pm t/lib/Test/Simple.pm DONOR-LICENSE
%{perl_vendorlib}/Class/Exporter.pm
%{_mandir}/man3/Class::Exporter.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Preserve original default test helpers and inherited exporter license terms.

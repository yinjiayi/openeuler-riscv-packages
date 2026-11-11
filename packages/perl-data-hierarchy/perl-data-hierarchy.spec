# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Hierarchy
Version:        0.34
Release:        1%{?dist}
Summary:        Handle inheritable data in a hierarchical structure
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Hierarchy
Source0:        Data-Hierarchy-0.34.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(Test::Exception)

%description
Handle inheritable data in a hierarchical structure

%prep
%autosetup -p1 -n Data-Hierarchy-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README
%doc CHANGES
%{perl_vendorlib}/Data/Hierarchy.pm
%{_mandir}/man3/Data::Hierarchy.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.34-1
- Package Data::Hierarchy with its original tests.

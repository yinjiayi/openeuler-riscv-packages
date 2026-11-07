# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-default
Version:        1.51
Release:        1%{?dist}
Summary:        Perl base class for default object instances
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Default
Source0:        https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Class-Default-%{version}.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Carp
BuildRequires:  perl-PathTools
BuildRequires:  perl-generators
Requires:       perl-Carp

%description
Class::Default lets methods called on a class use its default object instance,
while ordinary method calls continue to use the explicitly supplied instance.

%prep
%setup -q -n Class-Default-%{version}
%patch0 -p1

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
%license LICENSE BUNDLED-HELPER-NOTICES
%doc README Changes
%{perl_vendorlib}/Class/Default.pm
%{_mandir}/man3/Class::Default.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.51-1
- Package fixed upstream release with original tests and helper notices.

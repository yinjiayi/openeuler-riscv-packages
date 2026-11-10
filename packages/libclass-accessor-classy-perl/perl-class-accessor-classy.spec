# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-accessor-classy
Version:        0.9.1
Release:        1%{?dist}
Summary:        Declare read-only and writable Perl object accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Classy
Source0:        Class-Accessor-Classy-v0.9.1.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.28
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Carp)

%description
Class::Accessor::Classy declares named Perl object accessors with explicit
read-only or writable behavior.

%prep
%autosetup -n Class-Accessor-Classy-v%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir "%{buildroot}" --create_packlist=0

%check
./Build test --verbose

%files
%license lib/Class/Accessor/Classy.pm
%doc README Changes
%{perl_vendorlib}/Class/Accessor/Classy.pm
%{_mandir}/man3/Class::Accessor::Classy.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.1-1
- Package Class::Accessor::Classy 0.9.1 with its original default tests.

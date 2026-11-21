# SPDX-License-Identifier: Apache-2.0
Name:           libclass-pluggable-perl
Version:        0.022
Release:        1%{?dist}
Summary:        Add registered plugin methods and hooks to Perl objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Pluggable
Source0:        Class-Pluggable-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(vars)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(vars)

%description
Class::Pluggable lets a Perl application register preloaded plugin classes,
expose their exported methods, and dispatch named hooks on an object.

%prep
%autosetup -n Class-Pluggable-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run all original upstream default tests unchanged.
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Class/Pluggable.pm
%{_mandir}/man3/Class::Pluggable.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.022-1
- Package the official CPAN source with its original tests and license texts.

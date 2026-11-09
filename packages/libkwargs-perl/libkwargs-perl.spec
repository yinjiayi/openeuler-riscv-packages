# SPDX-License-Identifier: Apache-2.0
Name:           libkwargs-perl
Version:        0.01
Release:        1%{?dist}
Summary:        Handle named and positional keyword arguments in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Kwargs
Source0:        Kwargs-0.01.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Sub::Exporter)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Handle named and positional keyword arguments in Perl

%prep
%autosetup -n Kwargs-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Kwargs.pm
test -f %{buildroot}%{_mandir}/man3/Kwargs.3pm

%check
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README
%{perl_vendorlib}/Kwargs.pm
%{_mandir}/man3/Kwargs.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the verified release with its original tests and dual-license text.

# SPDX-License-Identifier: Apache-2.0
Name:           libhtml-tiny-perl
Version:        1.08
Release:        1%{?dist}
Summary:        Lightweight HTML and XML generation in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTML-Tiny
Source0:        HTML-Tiny-1.08.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.006
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(vars)
Requires:       perl >= 5.006
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Lightweight HTML and XML generation in Perl

%prep
%autosetup -n HTML-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/HTML/Tiny.pm
test -f %{buildroot}%{_mandir}/man3/HTML::Tiny.3pm

%check
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/HTML/Tiny.pm
%{_mandir}/man3/HTML::Tiny.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.08-1
- Package the original release with its complete default test suite.

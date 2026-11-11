# SPDX-License-Identifier: Apache-2.0
Name:           perl-any-uri-escape
Version:        0.01
Release:        1%{?dist}
Summary:        Select an available URI escaping implementation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Any-URI-Escape
Source0:        Any-URI-Escape-0.01.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(URI::Escape)
Requires:       perl(Exporter)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Any::URI::Escape exports URI escaping and unescaping. It uses URI::Escape
and selects the optional URI::Escape::XS implementation when available.

%prep
%autosetup -n Any-URI-Escape-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Any/URI/Escape.pm
test -f %{buildroot}%{_mandir}/man3/Any::URI::Escape.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Any/URI/Escape.pm
%{_mandir}/man3/Any::URI::Escape.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the pinned upstream release and retain all original default assertions.

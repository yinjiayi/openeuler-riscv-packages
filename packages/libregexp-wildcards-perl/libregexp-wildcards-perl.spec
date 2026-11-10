# SPDX-License-Identifier: Apache-2.0
Name:           libregexp-wildcards-perl
Version:        1.05
Release:        1%{?dist}
Summary:        Convert wildcard patterns into Perl regular expressions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Regexp-Wildcards
Source0:        Regexp-Wildcards-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::Balanced)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Scalar::Util)
Requires:       perl(Text::Balanced)

%description
Convert wildcard patterns into Perl regular expressions, with support for
shell-style wildcards, SQL wildcards and configurable captures.

%prep
%setup -q -n Regexp-Wildcards-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Regexp/Wildcards.pm
%{_mandir}/man3/Regexp::Wildcards.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.05-1
- Package the pinned release and run all original tests.

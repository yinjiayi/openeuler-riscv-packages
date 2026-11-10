# SPDX-License-Identifier: Apache-2.0
Name:           perl-time-clock
Version:        1.03
Release:        1%{?dist}
Summary:        Twenty-four-hour Perl clock object with nanosecond precision
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Time-Clock
Source0:        https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Time-Clock-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl
Requires:       perl(Carp)

%description
Time::Clock represents a time of day without a calendar date. It supports
parsing, formatting and arithmetic at nanosecond precision.

%prep
%setup -q -n Time-Clock-%{version}
sed -n '/^=head1 LICENSE$/,$p' lib/Time/Clock.pm > LICENSE-POD
test -s LICENSE-POD

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
perl -e 'use Test::Pod 1.00;'
make test

%files
%license LICENSE-POD
%doc Changes
%{perl_vendorlib}/Time/Clock.pm
%{_mandir}/man3/Time::Clock.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the fixed upstream release and retain the complete default tests.

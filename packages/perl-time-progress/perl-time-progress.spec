# SPDX-License-Identifier: Apache-2.0
Name:           perl-time-progress
Version:        2.15
Release:        1%{?dist}
Summary:        Perl progress meter and elapsed time reporter
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Time-Progress
Source0:        https://cpan.metacpan.org/authors/id/C/CA/CADE/Time-Progress-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl
Requires:       perl(Carp)

%description
Time::Progress formats task completion as a percentage or a progress meter.
It also reports elapsed time and estimates the remaining time.

%prep
%setup -q -n Time-Progress-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Time/Progress.pm
%{_mandir}/man3/Time::Progress.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.15-1
- Package the fixed upstream release and retain the complete default tests.

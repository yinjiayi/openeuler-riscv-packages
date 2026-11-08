# SPDX-License-Identifier: Apache-2.0
Name:           libtime-fake-perl
Version:        0.11
Release:        1%{?dist}
Summary:        Simulate time in Perl without changing the system clock
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-Fake
Source0:        Time-Fake-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Carp)

%description
Time::Fake offsets the clock seen by Perl's time, localtime, and gmtime
built-ins without changing the operating-system clock.

%prep
%autosetup -n Time-Fake-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run all original default assertions unchanged.
TZ=UTC make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Time/Fake.pm
%{_mandir}/man3/Time::Fake.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official CPAN source with its original tests and license texts.

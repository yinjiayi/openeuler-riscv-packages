# SPDX-License-Identifier: Apache-2.0
Name:           libtime-parsedate-perl
Version:        2026.033
Release:        1%{?dist}
Summary:        Parse date and time expressions in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-ParseDate
Source0:        Time-ParseDate-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        Module-Install-1.21.tar.gz
Source4:        Module-Install-ReadmeFromPod-0.30.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  tzdata
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::MockTime) >= 0.17
Requires:       perl
Requires:       perl(Time::Local)

%description
Time::ParseDate parses date and time expressions. The distribution also
supplies the original companion modules for formatting and calendar
calculations.

%prep
%autosetup -n Time-ParseDate-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt
# Preserve the donor notices without running code from the donor archives.
tar -xOf %{SOURCE3} Module-Install-1.21/lib/Module/Install.pod > Module-Install-NOTICE.txt
tar -xOf %{SOURCE4} Module-Install-ReadmeFromPod-0.30/LICENSE > ReadmeFromPod-LICENSE.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Preserve every original test, including simulated daylight-saving time.
TZ=PST8PDT LC_ALL=C make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%license Module-Install-NOTICE.txt ReadmeFromPod-LICENSE.txt
%doc Changes
%{perl_vendorlib}/Time/CTime.pm
%{perl_vendorlib}/Time/DaysInMonth.pm
%{perl_vendorlib}/Time/JulianDay.pm
%{perl_vendorlib}/Time/ParseDate.pm
%{perl_vendorlib}/Time/Timezone.pm
%{_mandir}/man3/Time::CTime.3pm*
%{_mandir}/man3/Time::DaysInMonth.3pm*
%{_mandir}/man3/Time::JulianDay.3pm*
%{_mandir}/man3/Time::ParseDate.3pm*
%{_mandir}/man3/Time::Timezone.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.033-1
- Package the official CPAN release with original tests and donor notices.

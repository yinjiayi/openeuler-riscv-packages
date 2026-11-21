# SPDX-License-Identifier: Apache-2.0
Name:           libtie-cycle-sinewave-perl
Version:        0.05
Release:        1%{?dist}
Summary:        Cycle a tied Perl scalar over a sine wave
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Cycle-Sinewave
Source0:        Tie-Cycle-Sinewave-0.05.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl
Requires:       perl(constant)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Tie::Cycle::Sinewave returns the next sample of a sine wave each time
the tied scalar is fetched and supports callbacks at the extrema.

%prep
%autosetup -n Tie-Cycle-Sinewave-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes TODO eg
%{perl_vendorlib}/Tie/Cycle/Sinewave.pm
%{_mandir}/man3/Tie::Cycle::Sinewave.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package the signed upstream release with its original MakeMaker default tests.

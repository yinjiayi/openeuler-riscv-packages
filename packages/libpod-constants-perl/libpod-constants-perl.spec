# SPDX-License-Identifier: Apache-2.0
Name:           libpod-constants-perl
Version:        0.19
Release:        1%{?dist}
Summary:        Extract constants from Perl POD sections
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Pod-Constants
Source0:        Pod-Constants-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Parser) >= 1.13
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Pod::Parser) >= 1.13

%description
Pod::Constants extracts selected POD sections into Perl variables or passes
their text to callbacks.

%prep
%autosetup -n Pod-Constants-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run the unchanged original default tests.
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Pod/Constants.pm
%{_mandir}/man3/Pod::Constants.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19-1
- Package the official CPAN release and run its original tests.

# SPDX-License-Identifier: Apache-2.0
Name:           libdns-zoneparse-perl
Version:        1.10
Release:        1%{?dist}
Summary:        Parse and edit DNS zone files in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/DNS-ZoneParse
Source0:        DNS-ZoneParse-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Storable) >= 0.407
BuildRequires:  perl(POSIX)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(vars)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.31
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Storable) >= 0.407
Requires:       perl(POSIX)
Requires:       perl(File::Basename)
Requires:       perl(vars)

%description
DNS::ZoneParse parses local DNS zone text into record objects and serializes
those records back into a zone file. It does not perform DNS lookups.

%prep
%autosetup -n DNS-ZoneParse-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run all original upstream default tests without modification.
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/DNS/ZoneParse.pm
%{_mandir}/man3/DNS::ZoneParse.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10-1
- Package the official release with its unchanged tests and full licenses.

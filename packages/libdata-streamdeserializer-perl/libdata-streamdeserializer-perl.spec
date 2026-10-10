# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-StreamDeserializer
Version:        0.06
Release:        1%{?dist}
Summary:        Incrementally deserialize Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-StreamDeserializer
Source0:        Data-StreamDeserializer-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Encode
BuildRequires:  perl-Time-HiRes
BuildRequires:  perl-generators

%description
Data::StreamDeserializer incrementally reconstructs Perl data structures
from serialized text without requiring a complete input buffer at once.

%prep
%autosetup -n Data-StreamDeserializer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all seven unchanged upstream default tests, including the memory check.
%make_build test

%files
%doc README Changes
%{perl_vendorarch}/Data/StreamDeserializer.pm
%{perl_vendorarch}/auto/Data/StreamDeserializer/
%{_mandir}/man3/Data::StreamDeserializer.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN XS release with the complete default test suite.

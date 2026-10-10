# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-MAC
Version:        2.103622
Release:        1%{?dist}
Summary:        Represent and manipulate MAC addresses in Perl
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/Net-MAC
Source0:        Net-MAC-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
Requires:       perl(Carp)
Requires:       perl(integer)
Requires:       perl(overload)

%description
Net::MAC represents MAC addresses and converts their base, grouping,
delimiter, and vendor-style display formats.

%prep
%autosetup -n Net-MAC-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all seven unchanged upstream tests, including POD and POD coverage.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Net/MAC.pm
%{_mandir}/man3/Net::MAC.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.103622-1
- Package official CPAN release with unchanged default upstream tests.

# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-Statsd
Version:        0.13
Release:        1%{?dist}
Summary:        UDP client for the statsd metric collector
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/Net-Statsd
Source0:        Net-Statsd-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(Time::HiRes)

%description
Net::Statsd sends counters, gauges, and timing values to a statsd collector
over UDP. The upstream benchmark utility is included but is not used for
target performance claims.

%prep
%autosetup -n Net-Statsd-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
mv %{buildroot}%{_bindir}/benchmark.pl %{buildroot}%{_bindir}/net-statsd-benchmark

%check
# Retain the four unchanged upstream default files, including local UDP and
# malformed-metric regression checks.
%make_build test

%files
%license LICENSE
%doc Changes README README.pod
%{perl_vendorlib}/Net/Statsd.pm
%{_bindir}/net-statsd-benchmark
%{_mandir}/man3/Net::Statsd.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Package official CPAN release with all four default upstream test files.

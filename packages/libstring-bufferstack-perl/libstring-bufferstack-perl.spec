# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-BufferStack
Version:        1.16
Release:        1%{?dist}
Summary:        Nested output buffers for Perl templating systems
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-BufferStack
Source0:        String-BufferStack-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::BufferStack holds nested output buffers. Frames can capture or
filter content before it reaches a caller-defined output method.

%prep
%autosetup -n String-BufferStack-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five default upstream test files, including capture and filter tests.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/String/BufferStack.pm
%{_mandir}/man3/String::BufferStack.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Package official CPAN release and retain all default upstream tests.

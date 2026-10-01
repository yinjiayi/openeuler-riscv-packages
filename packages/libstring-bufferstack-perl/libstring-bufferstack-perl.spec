# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-BufferStack
Version:        1.16
Release:        1%{?dist}
Summary:        Nested string buffers for templating systems
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-BufferStack
Source0:        String-BufferStack-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::BufferStack manages nested output buffers with optional filters and
callbacks for templating systems.

%prep
%autosetup -n String-BufferStack-%{version} -p1

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five unmodified default t/*.t files (169 declared assertions).
%make_build test

%files
%license lib/String/BufferStack.pm
%doc Changes README
%{perl_vendorlib}/String/BufferStack.pm
%{_mandir}/man3/String::BufferStack.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Package official CPAN release with complete default upstream tests.

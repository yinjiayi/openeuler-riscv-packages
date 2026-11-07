# SPDX-License-Identifier: Apache-2.0
Name:           perl-Regexp-IPv6
Version:        0.03
Release:        1%{?dist}
Summary:        Perl regular expression for IPv6 address syntax
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Regexp-IPv6
Source0:        Regexp-IPv6-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Regexp::IPv6 exports a regular expression for IPv6 addresses in RFC 2373
text representation. As documented upstream, the unspecified address ::
is excluded. Anchor the expression when matching an entire string.

%prep
%autosetup -n Regexp-IPv6-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Original 198-assertion suite, including its unchanged disabled TODO block.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Regexp/IPv6.pm
%{_mandir}/man3/Regexp::IPv6.3*

%changelog
* Fri Nov 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN release with the unchanged default test suite.

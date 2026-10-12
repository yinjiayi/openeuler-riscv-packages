# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Scanf
Version:        2.1
Release:        1%{?dist}
Summary:        C-style sscanf parsing for Perl strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Scanf
Source0:        String-Scanf-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
String::Scanf parses structured text with C-style sscanf format specifiers.
It supports a function interface and reusable parser objects.

%prep
%autosetup -n String-Scanf-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the complete upstream TAP suite (135 assertions in t/scanf.t).
%make_build test

%files
%license lib/String/Scanf.pm
%doc ChangeLog README
%{perl_vendorlib}/String/Scanf.pm
%{_mandir}/man3/String::Scanf.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1-1
- Package official CPAN release and retain the complete upstream test suite.

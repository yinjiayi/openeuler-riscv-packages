# SPDX-License-Identifier: Apache-2.0
Name:           libtest-more-utf8-perl
Version:        0.05
Release:        1%{?dist}
Summary:        Enable UTF-8 input and output for Perl Test::More
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-More-UTF8
Source0:        Test-More-UTF8-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Pod::Coverage) >= 0.18
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Test::More)

%description
Enable UTF-8 source text and UTF-8 output handles for Perl Test::More.
The module can enable all test output handles or a selected subset.

%prep
%setup -q -n Test-More-UTF8-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Test/More/UTF8.pm
%{_mandir}/man3/Test::More::UTF8.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package the pinned release and run the complete original suite.

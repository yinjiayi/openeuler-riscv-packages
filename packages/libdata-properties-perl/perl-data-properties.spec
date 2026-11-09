# SPDX-License-Identifier: Apache-2.0
Name:           perl-data-properties
Version:        1.07
Release:        1%{?dist}
Summary:        Read, write and retain persistent property lists in Perl
License:        Apache-2.0
URL:            https://metacpan.org/dist/Data-Properties
Source0:        Data-Properties-1.07.tar.gz
Source1:        LICENSE-2.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(POSIX)
Requires:       perl(strict)

%description
Read and write Java-style property lists in Perl, with defaults and
continuation lines.

%prep
%autosetup -n Data-Properties-%{version}
cp -p "%{SOURCE1}" LICENSE-APACHE-2.0

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE LICENSE-APACHE-2.0
%doc Changes
%{perl_vendorlib}/Data/Properties.pm
%{_mandir}/man3/Data::Properties.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package the exact signed Data::Properties 1.07 release with both licenses.

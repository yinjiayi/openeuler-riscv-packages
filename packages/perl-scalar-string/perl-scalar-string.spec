# SPDX-License-Identifier: Apache-2.0
Name:           perl-scalar-string
Version:        0.003
Release:        1%{?dist}
Summary:        Classify and change Perl scalar string encoding
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Scalar-String
Source0:        Scalar-String-0.003.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-Module-Build
BuildRequires:  perl-ExtUtils-CBuilder
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
Requires:       perl-Carp
Requires:       perl-Exporter
Requires:       perl-parent

%description
Scalar::String classifies the internal encoding of Perl strings and changes
between upgraded UTF-8 and downgraded representations while retaining their
characters. This package includes the upstream XS implementation and its
original pure-Perl fallback.

%prep
%setup -q -n Scalar-String-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build
test -f blib/arch/auto/Scalar/String/String.so

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license README
%doc Changes
%{perl_vendorarch}/Scalar/String.pm
%{perl_vendorarch}/auto/Scalar/String/
%{_mandir}/man3/Scalar::String.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003-1
- Package fixed official release; retain complete XS and fallback default tests.

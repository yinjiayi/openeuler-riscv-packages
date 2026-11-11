# SPDX-License-Identifier: Apache-2.0
Name:           perl-JSON-MultiValueOrdered
Version:        0.006
Release:        1%{?dist}
Summary:        JSON parser preserving ordered duplicate object keys
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/JSON-MultiValueOrdered
Source0:        JSON-MultiValueOrdered-0.006.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl
BuildArch:      noarch

%description
JSON parser preserving ordered duplicate object keys

%prep
%autosetup -p1 -n JSON-MultiValueOrdered-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE COPYRIGHT
%doc README Changes CREDITS
%{perl_vendorlib}/JSON/MultiValueOrdered.pm
%{perl_vendorlib}/JSON/Tiny/Subclassable.pm
%{perl_vendorlib}/Tie/Hash/MultiValueOrdered.pm
%{_mandir}/man3/JSON::MultiValueOrdered.3*
%{_mandir}/man3/JSON::Tiny::Subclassable.3*
%{_mandir}/man3/Tie::Hash::MultiValueOrdered.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package JSON::MultiValueOrdered with its original tests and notices.

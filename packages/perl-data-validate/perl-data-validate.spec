# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-data-validate
Version:        0.09
Release:        1%{?dist}
Summary:        Common numeric and string validation helpers for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Validate
Source0:        Data-Validate-%{version}.tar.gz
Patch0:         0001-retain-bundled-tbone-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Math-BigInt >= 1.77
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Exporter
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl-Math-BigInt >= 1.77
Requires:       perl-Scalar-List-Utils
Requires:       perl-Exporter

%description
Data::Validate provides common numeric and string validation helpers.
Success may return zero or an empty value: callers should check definedness.
It does not provide context-specific shell, SQL or HTML sanitization.

%prep
%setup -q -n Data-Validate-%{version}
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license README COPYING.TBone COPYING.Artistic COPYING.GPL1
%doc Changes INSTALL
%{perl_vendorlib}/Data/Validate.pm
%{perl_vendorlib}/auto/Data/Validate/
%{_mandir}/man3/Data::Validate.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Preserve all default tests and restore the bundled test-helper notices.

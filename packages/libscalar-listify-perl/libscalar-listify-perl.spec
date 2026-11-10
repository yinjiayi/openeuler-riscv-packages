# SPDX-License-Identifier: Apache-2.0
Name:           libscalar-listify-perl
Version:        0.03
Release:        1%{?dist}
Summary:        Convert a scalar or array reference into a Perl list
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Scalar-Listify
Source0:        Scalar-Listify-0.03.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(warnings)
BuildRequires:  perl(strict)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(Data::Dumper)
Requires:       perl(warnings)
Requires:       perl(strict)

%description
Convert a scalar or array reference into a Perl list or a new array reference.

%prep
%autosetup -n Scalar-Listify-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat <<'UPSTREAM_NOTICE' > Scalar-Listify-NOTICE
Copyright 1999-present by Terrence Brannon.

This library is free software; you can redistribute it and/or modify it under the same terms as Perl itself.
The original notice remains in Listify.pm.
UPSTREAM_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license Scalar-Listify-NOTICE Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Scalar/Listify.pm
%{_mandir}/man3/Scalar::Listify.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the signed official release with the unchanged legacy test.

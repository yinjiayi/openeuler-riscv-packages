# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Walk
Version:        2.01
Release:        1%{?dist}
Summary:        Traverse Perl data structures with callbacks
License:        LGPL-2.0-or-later AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Data-Walk
Source0:        Data-Walk-%{version}.tar.gz
Source1:        perl-5.8.7-README
Source2:        perl-5.8.7-Artistic
Source3:        perl-5.8.7-Copying
Patch0:         0001-document-inherited-perl-pod-origin.patch

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils >= 1.38
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators
Requires:       perl(Scalar::Util) >= 1.38

%description
Data::Walk traverses nested scalars, arrays, hashes and blessed structures,
with pre-order/depth-first callbacks and explicit cycle-handling options.

%prep
%setup -q -n Data-Walk-%{version}
# Documentation-only origin notice: no fuzzy application or executable edits.
%patch -P 0 -p1 -F 0
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve every upstream default .t file, assertion and feature.
%make_build test
# Mandatory Harness evaluates legacy Test TAP without accepting printed failure.
PERL5LIB="$PWD/blib/lib:$PWD/blib/arch" %{__perl} -MTest::Harness -e 'runtests(sort glob "t/*.t")'

%files
%license COPYING.LESSER perl-5.8.7-README perl-5.8.7-Artistic perl-5.8.7-Copying PERL-POD-ORIGIN
%doc ChangeLog NEWS README
%{perl_vendorlib}/Data/Walk.pm
%{_mandir}/man3/Data::Walk.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.01-1
- Add official release with unchanged complete tests and scoped origin notices.

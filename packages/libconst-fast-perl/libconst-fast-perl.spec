# SPDX-License-Identifier: Apache-2.0
Name:           libconst-fast-perl
Version:        0.014
Release:        1%{?dist}
Summary:        Facility for creating read-only Perl variables
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/LEONT/Const-Fast-0.014
Source0:        Const-Fast-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Module::Build::Tiny) >= 0.021
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Sub::Exporter::Progressive) >= 0.001007
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Carp)
Requires:       perl(Scalar::Util)
Requires:       perl(Storable)
Requires:       perl(Sub::Exporter::Progressive) >= 0.001007

%description
Const::Fast creates read-only Perl scalars, arrays and hashes. It preserves
recursive structure and rejects attempts to modify or reassign constants.

%prep
%autosetup -n Const-Fast-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build build

%install
%{__perl} Build install --destdir "%{buildroot}"
# Only generated installation bookkeeping for this module is unshipped.
find "%{buildroot}" -type f -path '*/auto/Const/Fast/.packlist' -delete

%check
%{__perl} Build test --verbose

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Const/Fast.pm
%{_mandir}/man3/Const::Fast.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.014-1
- Package the official release with the unmodified default test suite.

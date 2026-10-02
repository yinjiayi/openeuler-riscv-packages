# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-Encode
Version:        1.1.1
Release:        1%{?dist}
Summary:        Percent-encode and decode URI strings in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-Encode
Source0:        URI-Encode-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Encode) >= 2.12
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build) >= 0.38
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)
Requires:       perl(Encode) >= 2.12
Requires:       perl(Carp)

%description
URI::Encode provides object-oriented and function interfaces for percent
encoding and decoding URI strings.

%prep
%autosetup -n URI-Encode-v%{version}

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/URI/Encode.pm
%{_mandir}/man3/URI::Encode.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Package official CPAN source with unchanged upstream default tests.

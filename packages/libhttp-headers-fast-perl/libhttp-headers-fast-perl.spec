# SPDX-License-Identifier: Apache-2.0
Name:           perl-HTTP-Headers-Fast
Version:        0.22
Release:        1%{?dist}
Summary:        HTTP header container compatible with HTTP::Headers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTTP-Headers-Fast
Source0:        HTTP-Headers-Fast-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build::Tiny) >= 0.035
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(URI)
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Storable)
Requires:       perl(Carp)
Requires:       perl(HTTP::Date)
Requires:       perl(MIME::Base64)
Requires:       perl(Storable)

%description
HTTP::Headers::Fast is an HTTP header container with a compatible
HTTP::Headers-style interface and PSGI flattening helpers.

%prep
%autosetup -n HTTP-Headers-Fast-%{version}

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
%doc README.md Changes
%{perl_vendorlib}/HTTP/Headers/Fast.pm
%{_mandir}/man3/HTTP::Headers::Fast.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.22-1
- Package official CPAN source with unchanged upstream default tests.

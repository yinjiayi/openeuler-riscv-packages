# SPDX-License-Identifier: Apache-2.0
Name:           perl-HTTP-Tiny-Multipart
Version:        0.08
Release:        1%{?dist}
Summary:        Multipart POST helper for HTTP::Tiny
License:        Artistic-2.0
URL:            https://metacpan.org/dist/HTTP-Tiny-Multipart
Source0:        HTTP-Tiny-Multipart-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(MIME::Base64)
Requires:       perl(HTTP::Tiny)
Requires:       perl(Carp)
Requires:       perl(File::Basename)
Requires:       perl(MIME::Base64)

%description
HTTP::Tiny::Multipart adds a multipart/form-data POST helper to HTTP::Tiny.

%prep
%autosetup -n HTTP-Tiny-Multipart-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENSE
%doc Changes CONTRIBUTORS
%{perl_vendorlib}/HTTP/Tiny/Multipart.pm
%{_mandir}/man3/HTTP::Tiny::Multipart.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package official CPAN source with unchanged upstream default tests.

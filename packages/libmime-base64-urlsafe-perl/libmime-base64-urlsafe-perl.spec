# SPDX-License-Identifier: Apache-2.0
Name:           perl-MIME-Base64-URLSafe
Version:        0.01
Release:        1%{?dist}
Summary:        URL-safe Base64 encoder and decoder for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/MIME-Base64-URLSafe
Source0:        MIME-Base64-URLSafe-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(MIME::Base64)

%description
MIME::Base64::URLSafe encodes and decodes unpadded Base64 using URL-safe
characters, compatible with Python's URL-safe Base64 codec.

%prep
%autosetup -n MIME-Base64-URLSafe-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete upstream default suite (one t/*.t file, 17 assertions).
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/MIME/Base64/URLSafe.pm
%{_mandir}/man3/MIME::Base64::URLSafe.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the official CPAN release with its full default test suite.

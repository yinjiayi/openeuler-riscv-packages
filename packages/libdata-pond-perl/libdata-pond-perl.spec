# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Pond
Version:        0.006
Release:        1%{?dist}
Summary:        Perl-based open notation for data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Pond
Source0:        Data-Pond-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Params::Classify)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl-generators
Requires:       perl(Params::Classify)
Requires:       perl(XSLoader)

%description
Data::Pond reads and writes Pond, a restricted Perl-like textual notation
for strings, arrays, and hashes. It provides an XS implementation and an
upstream pure-Perl fallback.

%prep
%autosetup -n Data-Pond-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Use absolute blib paths so a loader policy cannot silently select the
# pure-Perl fallback for the non-pp upstream tests.
export PERL5LIB="$PWD/blib/lib:$PWD/blib/arch"
%{__perl} -MB -MData::Pond -e 'die "XS backend was not loaded\n" unless B::svref_2object(Data::Pond->can("pond_read_datum"))->XSUB'
# Preserve all nine unchanged upstream default tests, including forced-pp
# pairs; two author-only POD files self-skip without AUTHOR_TESTING.
./Build test

%files
%doc README Changes
%{perl_vendorarch}/Data/Pond.pm
%{perl_vendorarch}/auto/Data/Pond/
%{_mandir}/man3/Data::Pond.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package official CPAN release with XS and unchanged pure-Perl fallback tests.

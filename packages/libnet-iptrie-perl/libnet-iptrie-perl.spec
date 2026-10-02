# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-IPTrie
Version:        0.7
Release:        1%{?dist}
Summary:        IPv4 and IPv6 prefix trie for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-IPTrie
Source0:        Net-IPTrie-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-NetAddr-IP
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-bignum
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(NetAddr::IP) >= 4.007
Requires:       perl(Scalar::Util) >= 1.21
Requires:       perl(Class::Struct) >= 0.63
Requires:       perl(bigint)

%description
Net::IPTrie provides a Perl radix tree for IPv4 and IPv6 prefixes, including
insertion, closest-prefix lookup, parent traversal, and deletion.

%prep
%autosetup -n Net-IPTrie-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole original upstream test and its Node.pm:60 warnings.
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Net/IPTrie.pm
%{perl_vendorlib}/Net/IPTrie/
%{_mandir}/man3/Net::IPTrie*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7-1
- Package official CPAN release with its unchanged default upstream test.

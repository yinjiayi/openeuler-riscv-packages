# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-aliashash
Version:        1.02
Release:        1%{?dist}
Summary:        Perl tied hash with multiple keys for a single value
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Tie-AliasHash
Source0:        Tie-AliasHash-1.02.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Tie::AliasHash provides a Perl tied hash in which one value can be read
or updated by more than one key.

%prep
%autosetup -n Tie-AliasHash-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test verbose=1

%files
%license Artistic-1.0-Perl.txt GPL-1.0.txt
%doc README Changes
%{perl_vendorlib}/Tie/AliasHash.pm
%{_mandir}/man3/Tie::AliasHash.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package the verified CPAN release and retain its default test action.

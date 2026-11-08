# SPDX-License-Identifier: Apache-2.0
Name:           libtie-shadowhash-perl
Version:        2.01
Release:        1%{?dist}
Summary:        Combine multiple Perl hash sources with isolated overrides
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND MIT AND FSFAP
URL:            https://metacpan.org/dist/Tie-ShadowHash
Source0:        Tie-ShadowHash-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt

BuildArch:      noarch
BuildRequires:  perl >= 5.24.0
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.28
BuildRequires:  perl(autodie)
BuildRequires:  perl(Carp)
BuildRequires:  perl(AnyDBM_File)
BuildRequires:  perl(NDBM_File)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
Requires:       perl >= 5.24.0
Requires:       perl(autodie)
Requires:       perl(Carp)

%description
Tie::ShadowHash combines multiple hash-like sources. Lookups use source
order, and local overrides and deletions do not modify the original sources.

%prep
%autosetup -n Tie-ShadowHash-%{version} -p1
cp -p %{SOURCE1} Artistic-1.0-Perl.txt
cp -p %{SOURCE2} GPL-1.0.txt

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --destdir=%{buildroot} --create_packlist=0

%check
# Run the upstream recursive default suite, preserving its original gates.
%{__perl} Build test --verbose

%files
%license LICENSE Artistic-1.0-Perl.txt GPL-1.0.txt
%doc README README.md Changes
%{perl_vendorlib}/Tie/ShadowHash.pm
%{_mandir}/man3/Tie::ShadowHash.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.01-1
- Package the official source, unchanged tests, and complete rights notices.

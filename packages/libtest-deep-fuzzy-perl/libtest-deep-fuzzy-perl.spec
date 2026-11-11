# SPDX-License-Identifier: Apache-2.0
Name:           libtest-deep-fuzzy-perl
Version:        0.01
Release:        1%{?dist}
Summary:        Fuzzy number comparison with Test::Deep
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/KARUPA/Test-Deep-Fuzzy-0.01
Source0:        Test-Deep-Fuzzy-%{version}.tar.gz
Source1:        Minilla-v3.0.4-LICENSE.txt
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(B)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Math::Round)
BuildRequires:  perl(Module::Build::Tiny) >= 0.035
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Deep::Cmp)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(B)
Requires:       perl(Exporter) >= 5.57
Requires:       perl(Math::Round)
Requires:       perl(Scalar::Util)
Requires:       perl(Test::Deep::Cmp)

%description
Test::Deep::Fuzzy supplies a Test::Deep comparator that rounds floating-point
values to a configurable step before comparing.

%prep
%autosetup -n Test-Deep-Fuzzy-%{version} -p1
cp -p %{SOURCE1} .

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build build

%install
%{__perl} Build install --destdir "%{buildroot}"
# Only the generated package-specific ExtUtils::Install bookkeeping is omitted.
find "%{buildroot}" -type f -path '*/auto/Test/Deep/Fuzzy/.packlist' -delete

%check
%{__perl} Build test --verbose

%files
%license LICENSE Minilla-v3.0.4-LICENSE.txt
%doc README.md Changes
%{perl_vendorlib}/Test/Deep/Fuzzy.pm
%{perl_vendorlib}/Test/Deep/Fuzzy/Number.pm
%{_mandir}/man3/Test::Deep::Fuzzy.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the fixed upstream archive with all default tests and donor notices.

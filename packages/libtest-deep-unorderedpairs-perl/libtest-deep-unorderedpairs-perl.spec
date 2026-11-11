# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-deep-unorderedpairs
Version:        0.006
Release:        1%{?dist}
Summary:        Compare unordered tuples with Test::Deep
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0 AND Artistic-2.0
URL:            https://metacpan.org/release/ETHER/Test-Deep-UnorderedPairs-0.006
Source0:        Test-Deep-UnorderedPairs-%{version}.tar.gz
Source1:        Dist-Zilla-6.008.LICENSE
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.025.LICENSE
Source3:        Dist-Zilla-Plugin-InstallGuide-1.200007.LICENSE
Source4:        Dist-Zilla-PluginBundle-Author-ETHER-0.121.LICENCE
Source5:        Dist-Zilla-Plugin-Test-CPAN-Changes-0.012.LICENSE
Source6:        Dist-Zilla-Plugin-Test-CleanNamespaces-0.006.LICENSE
Source7:        Dist-Zilla-Plugin-Test-Compile-2.056.LICENCE
Source8:        Dist-Zilla-Plugin-Test-EOL-0.19.LICENCE
Source9:        Dist-Zilla-Plugin-Test-Kwalitee-2.12.LICENSE
Source10:       Dist-Zilla-Plugin-MojibakeTests-0.8.LICENSE
Source11:       Dist-Zilla-Plugin-Test-NoTabs-0.15.LICENSE
Source12:       Dist-Zilla-Plugin-Test-Pod-No404s-1.003.LICENSE
Source13:       Dist-Zilla-Plugin-Test-PodSpelling-2.007004.LICENCE
Source14:       Dist-Zilla-Plugin-Test-Portability-2.001000.LICENSE
Source15:       Dist-Zilla-Plugin-Test-MinimumVersion-2.000007.LICENSE
Source16:       Dist-Zilla-Plugin-Test-Synopsis-2.000007.LICENSE
Source17:       Dist-Zilla-Plugin-CheckChangesHasContent-0.010.LICENSE
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.006
BuildRequires:  perl-generators
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Deep::ArrayLength)
BuildRequires:  perl(Test::Deep::Cmp)
BuildRequires:  perl(Test::Deep::Set)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Exporter) >= 5.57
%description
Test::Deep::UnorderedPairs compares an unordered list of key/value tuples
with Test::Deep, including repeated keys.

%prep
%autosetup -n Test-Deep-UnorderedPairs-%{version} -p1
mkdir -p vendor-licenses
install -pm0644 %{SOURCE1} vendor-licenses/Dist-Zilla-6.008.LICENSE
install -pm0644 %{SOURCE2} vendor-licenses/Dist-Zilla-Plugin-Test-ReportPrereqs-0.025.LICENSE
install -pm0644 %{SOURCE3} vendor-licenses/Dist-Zilla-Plugin-InstallGuide-1.200007.LICENSE
install -pm0644 %{SOURCE4} vendor-licenses/Dist-Zilla-PluginBundle-Author-ETHER-0.121.LICENCE
install -pm0644 %{SOURCE5} vendor-licenses/Dist-Zilla-Plugin-Test-CPAN-Changes-0.012.LICENSE
install -pm0644 %{SOURCE6} vendor-licenses/Dist-Zilla-Plugin-Test-CleanNamespaces-0.006.LICENSE
install -pm0644 %{SOURCE7} vendor-licenses/Dist-Zilla-Plugin-Test-Compile-2.056.LICENCE
install -pm0644 %{SOURCE8} vendor-licenses/Dist-Zilla-Plugin-Test-EOL-0.19.LICENCE
install -pm0644 %{SOURCE9} vendor-licenses/Dist-Zilla-Plugin-Test-Kwalitee-2.12.LICENSE
install -pm0644 %{SOURCE10} vendor-licenses/Dist-Zilla-Plugin-MojibakeTests-0.8.LICENSE
install -pm0644 %{SOURCE11} vendor-licenses/Dist-Zilla-Plugin-Test-NoTabs-0.15.LICENSE
install -pm0644 %{SOURCE12} vendor-licenses/Dist-Zilla-Plugin-Test-Pod-No404s-1.003.LICENSE
install -pm0644 %{SOURCE13} vendor-licenses/Dist-Zilla-Plugin-Test-PodSpelling-2.007004.LICENCE
install -pm0644 %{SOURCE14} vendor-licenses/Dist-Zilla-Plugin-Test-Portability-2.001000.LICENSE
install -pm0644 %{SOURCE15} vendor-licenses/Dist-Zilla-Plugin-Test-MinimumVersion-2.000007.LICENSE
install -pm0644 %{SOURCE16} vendor-licenses/Dist-Zilla-Plugin-Test-Synopsis-2.000007.LICENSE
install -pm0644 %{SOURCE17} vendor-licenses/Dist-Zilla-Plugin-CheckChangesHasContent-0.010.LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# The original prereq report loads its own static fixture by relative path.
# Bind the reviewed release root only for this test process and its children.
PERL5LIB="$PWD" make test TEST_VERBOSE=1

%files
%license LICENCE vendor-licenses/*
%doc README Changes
%{perl_vendorlib}/Test/Deep/UnorderedPairs.pm
%{_mandir}/man3/Test::Deep::UnorderedPairs.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package the fixed CPAN release with original default tests and template terms.

# SPDX-License-Identifier: Apache-2.0
Name:           julius-speech
Version:        4.6
Release:        7%{?dist}
Summary:        A high-performance, two-pass large vocabulary continuous speech recognition decoder software
License:        BSD-3-Clause
URL:            https://github.com/julius-speech/julius
Source0:        julius-speech-4.6.tar.gz
Patch0:         patches/0001-libsent-restrict-cpuid-header-to-x86.patch
Patch1:         patches/0002-libsent-include-openmp-header-when-enabled.patch
Patch2:         patches/0003-fedora-support-destdir.patch
BuildRequires:  gcc
BuildRequires:  make

%description
A high-performance, two-pass large vocabulary continuous speech recognition decoder software

%prep
%autosetup -n julius-%{version} -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
export LC_ALL=C
./libsent/libsent-config --version | grep -F 'Julius/Julian libsent library rev.4.6'
./libjulius/libjulius-config --version | grep -F 'Julius/Julian library rev.4.6'
set +e
./julius/julius -help > julius-help.log 2>&1
help_rc=$?
set -e
test "$help_rc" -eq 1
grep -F 'Julius rev.4.6' julius-help.log
grep -F 'Speech Input:' julius-help.log

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-7
- Replace the nonexistent top-level check target with deterministic checks of
  the built decoder and generated library configuration reporters.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-6
- Import Fedora's downstream DESTDIR support for staged RPM installation.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-5
- Include omp.h whenever OpenMP is enabled on non-SIMD targets.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-4
- Regenerate the CPUID patch hunk with strict GNU patch-compatible context.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-3
- Restrict the x86-only cpuid.h include so RISC-V uses the existing scalar DNN path.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-2
- Match the SPEC source root to the verified archive's julius-4.6 top-level directory.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-1
- Initial openEuler RISC-V package from the full package inventory.

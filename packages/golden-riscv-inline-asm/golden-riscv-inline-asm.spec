# SPDX-License-Identifier: Apache-2.0
Name:           golden-riscv-inline-asm
Version:        1.0
Release:        2%{?dist}
Summary:        Deterministic x86-only inline assembly repair fixture
License:        MIT
URL:            https://github.com/yinjiayi/openeuler-riscv-packages/tree/main/tests/golden
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-riscv-use-rdcycle.patch

BuildRequires:  gcc
BuildRequires:  make

%description
This fixed fixture contains an intentional architecture branch failure. The
local repair workflow must add the one expected RISC-V patch without weakening
the test.

%prep
%autosetup -p1

%build
%make_build CFLAGS="%{optflags}"

%install
install -Dpm0755 golden-inline %{buildroot}%{_bindir}/golden-inline

%check
./golden-inline | grep -E '^[0-9]+$'

%files
%license LICENSE
%doc README.md
%{_bindir}/golden-inline

%changelog
* Sat Aug 08 2026 Package Automation <noreply@example.invalid> - 1.0-2
- Add the minimal RISC-V rdcycle repair after the observed target failure
- Use distribution optflags so RPM debugsource generation is non-empty

* Sat Aug 08 2026 Package Automation <noreply@example.invalid> - 1.0-1
- Add the intentionally failing RISC-V repair golden fixture

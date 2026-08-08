# SPDX-License-Identifier: Apache-2.0
Name:           checksec
Version:        3.2.0
Release:        1%{?dist}
Summary:        Inspect ELF binaries for hardening features
License:        BSD-3-Clause
URL:            https://github.com/slimm609/checksec.sh
Source0:        checksec-3.2.0.tar.gz

BuildRequires:  golang

%description
checksec audits ELF binaries, running processes, and Linux kernels for common
hardening features.

%prep
%autosetup -p1

%build
export CGO_ENABLED=0
export GOOS=linux
export GOARCH=riscv64
export GOTOOLCHAIN=local
export GOPROXY=off
go build -mod=readonly -buildmode=pie \
  -ldflags="-s -w -X main.version=%{version}" \
  -o checksec .

%install
install -Dpm0755 checksec %{buildroot}%{_bindir}/checksec
install -Dpm0644 extras/man/checksec.1 %{buildroot}%{_mandir}/man1/checksec.1

%check
./checksec --version | grep -F '%{version}'

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/checksec
%{_mandir}/man1/checksec.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.0-1
- Initial openEuler RISC-V package.

# SPDX-License-Identifier: Apache-2.0
Name:           checksec
Version:        3.2.0
Release:        2%{?dist}
Summary:        Inspect ELF binaries for hardening features
License:        BSD-3-Clause
URL:            https://github.com/slimm609/checksec.sh
Source0:        3.2.0.tar.gz

BuildRequires:  golang
BuildRequires:  jq

%description
checksec inspects ELF binaries, processes, and kernel configuration for common
hardening features. This package builds the upstream 3.2.0 Go implementation;
the legacy shell implementation retained in the source archive is not shipped.

%prep
%autosetup -p1

%build
export CGO_ENABLED=0
export GOTOOLCHAIN=go1.25.0+auto
export GOFLAGS='-mod=readonly'
go build -buildmode=pie -buildvcs=false -trimpath \
  -ldflags '-X main.version=%{version} -X main.commit=source -X main.date=reproducible' \
  -o checksec ./main.go

%install
install -Dpm0755 checksec %{buildroot}%{_bindir}/checksec
install -Dpm0644 extras/man/checksec.1 %{buildroot}%{_mandir}/man1/checksec.1

%check
export CGO_ENABLED=0
export GOTOOLCHAIN=go1.25.0+auto
export GOFLAGS='-mod=readonly'
go test -count=1 ./...
./checksec --version | grep -F '%{version}'
./checksec --no-banner --output json file /usr/bin/bash | \
  jq -e 'type == "array" and length == 1 and (.[0].checks | type == "object")'

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/checksec
%{_mandir}/man1/checksec.1*

%changelog
* Sun Sep 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.0-2
- Build the actual upstream Go implementation and run its complete Go test suite.

* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.0-1
- Initial automated update proposal.

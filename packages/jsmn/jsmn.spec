# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           jsmn
Version:        1.1.0
Release:        1%{?dist}
Summary:        Minimalistic JSON parser and tokenizer for C
License:        MIT
URL:            https://github.com/zserge/jsmn
Source0:        jsmn-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  make

%description
jsmn is a small, dependency-free, single-header JSON parser for C. It tokenizes
JSON without allocating or copying the input data.

%prep
%autosetup -p1

%build
# Header-only library; the target compiler is exercised by the test suite.

%install
install -Dpm0644 jsmn.h %{buildroot}%{_includedir}/jsmn/jsmn.h

%check
%make_build test CC=%{__cc} CFLAGS="%{optflags}"

%files
%license LICENSE
%doc README.md
%{_includedir}/jsmn/

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial package from the official 1.1.0 tag archive.
- Preserve all four upstream parser test modes in the target build.

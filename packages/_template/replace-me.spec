# SPDX-License-Identifier: Apache-2.0
Name:           replace-me
Version:        0.0.0
Release:        1%{?dist}
Summary:        Replace with a concise package summary
License:        SPDX-expression
URL:            https://example.invalid/replace-me
Source0:        replace-me-0.0.0.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Replace this text with a factual upstream description.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%{_builddir}/%{name}-%{version}/tests/smoke-test

%files
%license LICENSE*
%doc README*
%{_bindir}/replace-me

%changelog
* Sat Aug 08 2026 Package Automation <noreply@example.invalid> - 0.0.0-1
- Initial openEuler RISC-V package

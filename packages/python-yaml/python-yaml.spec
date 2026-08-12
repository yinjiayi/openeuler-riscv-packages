# SPDX-License-Identifier: Apache-2.0
Name:           python-yaml
Version:        6.0.3
Release:        1%{?dist}
Summary:        Python YAML parser and emitter with LibYAML bindings
License:        MIT
URL:            https://github.com/yaml/pyyaml
Source0:        pyyaml-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libyaml-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools

%description
PyYAML parses and emits YAML 1.1 data and provides both a Python
implementation and accelerated bindings to LibYAML.

%package -n python3-pyyaml
Summary:        Python 3 YAML parser and emitter
Provides:       python3-yaml = %{version}-%{release}

%description -n python3-pyyaml
PyYAML for Python 3 with the accelerated LibYAML extension enabled.

%prep
%autosetup -p1 -n pyyaml-49790e73684bebad1df05ef8d828fa12f685bffb

%build
export PYYAML_FORCE_LIBYAML=1
%py3_build

%install
export PYYAML_FORCE_LIBYAML=1
%py3_install

%check
export PYTHONPATH=%{buildroot}%{python3_sitearch}
%{python3} -c 'import yaml, yaml._yaml; assert yaml.__with_libyaml__'
%{python3} -m pytest -v

%files -n python3-pyyaml
%license LICENSE
%doc CHANGES README.md examples/
%{python3_sitearch}/yaml/
%{python3_sitearch}/_yaml/
%{python3_sitearch}/PyYAML-%{version}-py*.egg-info

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.3-1
- Update the target package with LibYAML and the complete upstream tests.

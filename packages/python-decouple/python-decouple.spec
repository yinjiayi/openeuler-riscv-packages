# SPDX-License-Identifier: Apache-2.0
Name:           python-decouple
Version:        3.8
Release:        1%{?dist}
Summary:        Strict separation of settings from code
License:        MIT
URL:            https://github.com/henriquebastos/python-decouple
Source0:        python-decouple-3.8.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
Requires:       python3
Requires:       python3-pytest
Requires:       python3-mock
BuildArch:      noarch

%description
Decouple separates application configuration from source code. The complete
official fixed release, original default suite and fixtures are retained.

%prep
%autosetup -n python-decouple-860969c0bc7ea9f6815447b498cbaf206813865b

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot} --prefix %{_prefix}
# Preserve only the immutable archive, not generated build/lib copies.
install -d %{buildroot}%{_datadir}/%{name}/original
tar -xf %{SOURCE0} --strip-components=1 -C %{buildroot}%{_datadir}/%{name}/original
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
# Whole original tox test command; no new selectors, skips or assertions removed.
py.test

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/decouple.py
%{python3_sitelib}/__pycache__/decouple.*.pyc
%{python3_sitelib}/python_decouple-*.egg-info/
%{_datadir}/%{name}/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8-1
- Pin the full official release and preserve complete original defaults.

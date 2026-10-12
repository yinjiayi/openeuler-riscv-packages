# SPDX-License-Identifier: Apache-2.0
Name:           python-ratelimit
Version:        2.2.1
Release:        1%{?dist}
Summary:        API rate limit decorator for Python
License:        MIT
URL:            https://github.com/tomasbasham/ratelimit
Source0:        ratelimit-2.2.1.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pylint
Requires:       python3
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-pylint
BuildArch:      noarch

%description
Ratelimit provides a function decorator limiting API calls. The complete
official release and original default test/configuration are retained.

%prep
%autosetup -n ratelimit-1cddcbd9708cdab583551f0bc5a0d40d7ed2eaa3

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot} --prefix %{_prefix}
install -d %{buildroot}%{_datadir}/%{name}/tests/unit
install -m 0644 tests/__init__.py %{buildroot}%{_datadir}/%{name}/tests/
install -m 0644 tests/unit/__init__.py tests/unit/decorator_test.py %{buildroot}%{_datadir}/%{name}/tests/unit/
install -m 0644 pytest.ini requirements.txt setup.py .pylintrc .travis.yml MANIFEST.in README.rst LICENSE.txt %{buildroot}%{_datadir}/%{name}/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
# Original Travis command and pytest.ini defaults, without new filters/skips.
# Target supplied tools, not the unsatisfied historical dev-pin equalities.
py.test

%files
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/ratelimit/
%{python3_sitelib}/ratelimit-*.egg-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-1
- Pin the complete official release and preserve whole original defaults.

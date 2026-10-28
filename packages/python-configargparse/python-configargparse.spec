# SPDX-License-Identifier: Apache-2.0
Name:           python-configargparse
Version:        1.9.0
Release:        1%{?dist}
Summary:        Argument parser with configuration-file and environment-variable support
License:        MIT
URL:            https://github.com/bw2/ConfigArgParse
Source0:        configargparse-1.9.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-black
BuildRequires:  python3-mock
BuildRequires:  python3-toml
BuildRequires:  python3-pyyaml
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-subtests
BuildRequires:  python3-coverage
Requires:       python3
Requires:       python3-devel
Requires:       python3-black
Requires:       python3-mock
Requires:       python3-toml
Requires:       python3-pyyaml
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-pytest-subtests
Requires:       python3-coverage

%description
ConfigArgParse extends argparse with configuration-file and environment-variable
support. The full official source archive and complete original target-Python3.11
default tests are retained, including argparse compatibility tests.

%prep
%autosetup -n ConfigArgParse-eba8686d82c007569f93b82c43a686ad7f68f6b3

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
# Standard supplied setuptools-scm release input for the immutable Git archive.
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
python3 setup.py bdist_wheel

%install
# Wheel/pip versions may preserve the original ConfigArgParse spelling or
# normalize it. Require one fresh wheel rather than guessing its case/tag.
set -- dist/*.whl
test "$#" -eq 1
test -f "$1"
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} "$1"
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/upstream.tar.gz

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
# Fail rather than accept upstream's missing stdlib compatibility-test fallback.
python3 -c 'import test.test_argparse, inspect; assert inspect.getsource(test.test_argparse)'
# Exact complete original selected Python3.11 CI argv; no test-selection/waiver.
pytest --cov-branch --cov-context=test --cov=.

%files
%license LICENSE
%doc README.md CONTRIBUTING.rst
%{python3_sitelib}/configargparse.py
%{python3_sitelib}/__pycache__/configargparse*.pyc
%{python3_sitelib}/[Cc]onfig[Aa]rg[Pp]arse-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Mon Oct 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.0-1
- Pin the full official release and preserve the complete original 3.11 test route.

# SPDX-License-Identifier: Apache-2.0
Name:           python-sentinels
Version:        1.1.1
Release:        1%{?dist}
Summary:        Singleton sentinel objects for special Python values
License:        BSD-3-Clause
URL:            https://github.com/vmalloc/sentinels
Source0:        sentinels-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-pytest
BuildRequires:  python3-pylint

%description
Sentinels provides named singleton objects for special Python values. Copying
and pickling preserve their identity, allowing defaults distinct from None.

%package -n python3-sentinels
Summary:        Singleton sentinel objects for special Python values
Requires:       python3 >= 3.9

%description -n python3-sentinels
Sentinels provides named singleton objects for special Python values.

%prep
%autosetup -n sentinels-%{version}

%build
# The pinned sdist includes PKG-INFO for hatch-vcs version resolution.
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip wheel --no-build-isolation --no-deps --wheel-dir dist .

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/sentinels-%{version}-py3-none-any.whl

%check
# Preserve both commands from upstream ci.yml, without test filtering/skips.
# The module resolves __version__ from installed distribution metadata.
export PYTHONPATH=%{buildroot}%{python3_sitelib}:$PWD
%{__python3} -m pytest -v tests
%{__python3} -m pylint --rcfile=.pylintrc sentinels tests

%files -n python3-sentinels
%license LICENSE
%doc README.md
%{python3_sitelib}/sentinels/
%{python3_sitelib}/sentinels-%{version}.dist-info/

%changelog
* Fri Oct 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Onboard the verified official sdist with full upstream test and lint commands.

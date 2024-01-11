Name:           python-tomli
Version:        2.0.1
Release:        5%{?dist}
Summary:        A little TOML parser for Python

License:        MIT
URL:            https://pypi.org/project/tomli/
Source0:        https://github.com/hukkin/tomli/archive/%{version}/%{name}-%{version}.tar.gz

# Upstream tomli uses flit, but we want to use setuptools on RHEL 9.
# This a downstream-only setup.py manually created from pyproject.toml metadata.
# It contains a @@VERSION@@ placeholder.
Source1:        tomli-setup.py

BuildArch:      noarch
BuildRequires:  python3-devel

# The test suite uses the stdlib's unittest framework, but we use %%pytest
# as the test runner.
BuildRequires:  python3-pytest

%global _description %{expand:
Tomli is a Python library for parsing TOML.
Tomli is fully compatible with TOML v1.0.0.}


%description %_description

%package -n python3-tomli
Summary:        %{summary}

%description -n python3-tomli %_description


%prep
%autosetup -p1 -n tomli-%{version}
sed 's/@@VERSION@@/%{version}/' %{SOURCE1} > setup.py
rm pyproject.toml  # force the PEP 517 fallback build backend (setuptools)


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tomli


%check
%py3_check_import tomli
%pytest


%files -n python3-tomli -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md


%changelog
* Wed Mar 08 2023 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-5
- Initial package for RHEL 9
- Resolves: rhbz#2175213
- Fedora+EPEL contributions by:
      Maxwell G <gotmax@e.email>
      Michel Alexandre Salim <salimma@fedoraproject.org>
      Miro Hrončok <miro@hroncok.cz>
      Petr Viktorin <pviktori@redhat.com>

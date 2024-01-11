Name:           python-tomli
Version:        1.2.3
Release:        4%{?dist}
Summary:        A little TOML parser for Python

License:        MIT
URL:            https://pypi.org/project/tomli/
%global forgeurl https://github.com/hukkin/tomli
Source0:        %{forgeurl}/archive/%{version}/%{name}-%{version}.tar.gz

# Upstream tomli uses flit, but we want to use setuptools on RHEL 8.
# This a downstream-only setup.py manually created from pyproject.toml metadata.
# It contains a @@VERSION@@ placeholder.
Source1:        tomli-setup.py

# RHEL 8's pytest is too old and does not support the tmp_path filter.
Patch0:         0001-tests-Replace-tmp_path-with-tmpdir-pytest-fixture.patch
# RHEL 8's old dateutil is missing parser.isoparse.
# This upstream change removes that test dependency entirely.
Patch1:         %{forgeurl}/commit/a54d95e.patch#/Remove_python-dateutil_test_dependency.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

# Upstream test requirements are in tests/requirements.txt
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


%build
%py3_build


%install
%py3_install


%check
%pytest


%files -n python3-tomli
%doc README.md
%doc CHANGELOG.md
%license LICENSE
%{python3_sitelib}/tomli/
%{python3_sitelib}/tomli-%{version}-py%{python3_version}.egg-info/


%changelog
* Wed Mar 08 2023 Miro Hrončok <mhroncok@redhat.com> - 1.2.3-4
- Initial package for RHEL 8
- Resolves: rhbz#2175215
- Fedora+EPEL contributions by:
      Maxwell G <gotmax@e.email>
      Miro Hrončok <miro@hroncok.cz>
      Petr Viktorin <pviktori@redhat.com>

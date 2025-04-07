#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_with	tests	# pytest tests
%bcond_without	doc	# Sphinx documentation

Summary:	The modular source code checker: pycodestyle, pyflakes and co.
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pycodestyle, pyflakes itp.
Name:		flake8
# before updating to 4.x fork python-flake8.spec with last 3.x version
Version:	3.9.2
Release:	5
License:	MIT
Group:		Development/Tools
#Source0Download: https://pypi.org/simple/flake8/
Source0:	https://files.pythonhosted.org/packages/source/f/flake8/%{name}-%{version}.tar.gz
# Source0-md5:	5c102972d3d0f35255c56a20613fcec5
Patch0:		%{name}-duplicate.patch
URL:		https://gitlab.com/pycqa/flake8
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:30
%if %{with tests}
BuildRequires:	python-configparser
BuildRequires:	python-enum34
BuildRequires:	python-functools32
BuildRequires:	python-importlib_metadata
BuildRequires:	python-mccabe >= 0.6.0
BuildRequires:	python-mccabe < 0.7.0
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-pycodestyle >= 2.7.0
BuildRequires:	python-pycodestyle < 2.8.0
BuildRequires:	python-pyflakes >= 2.3.0
BuildRequires:	python-pyflakes < 2.4.0
BuildRequires:	python-pytest
BuildRequires:	python-typing
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:30
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-mccabe >= 0.6.0
BuildRequires:	python3-mccabe < 0.7.0
BuildRequires:	python3-pycodestyle >= 2.7.0
BuildRequires:	python3-pycodestyle < 2.8.0
BuildRequires:	python3-pyflakes >= 2.3.0
BuildRequires:	python3-pyflakes < 2.4.0
BuildRequires:	python3-pytest
BuildRequires:	sed >= 4.0
%endif
%endif
%if %{with doc}
BuildRequires:	python3-sphinx-prompt
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
%if %{with python3}
Requires:	python3-flake8 = %{version}-%{release}
%else
Requires:	python-flake8 = %{version}-%{release}
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pycodestyle
- Ned Batchelder's McCabe script

%description -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pycodestyle
- skrypt McCabe autorstwa Neda Batcheldera

%package -n python-flake8
Summary:	The modular source code checker: pycodestyle, pyflakes and co.
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pycodestyle, pyflakes itp.
Group:		Libraries/Python
Requires:	python-mccabe >= 0.6.0
Requires:	python-mccabe < 0.7.0
Requires:	python-modules >= 1:2.7
Requires:	python-pycodestyle >= 2.7.0
Requires:	python-pycodestyle < 2.8.0
Requires:	python-pyflakes >= 2.3.0
Requires:	python-pyflakes < 2.4.0

%description -n python-flake8
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pycodestyle
- Ned Batchelder's McCabe script

%description -n python-flake8 -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pycodestyle
- skrypt McCabe autorstwa Neda Batcheldera

%package -n python3-flake8
Summary:	The modular source code checker: pycodestyle, pyflakes and co
Summary(pl.UTF-8):	Modularne narzędzie do sprawdzania kodu źródłowego: pycodestyle, pyflakes itp.
Group:		Libraries/Python
Requires:	python3-mccabe >= 0.6.0
Requires:	python3-mccabe < 0.7.0
Requires:	python3-modules >= 1:3.4
Requires:	python3-pycodestyle >= 2.7.0
Requires:	python3-pycodestyle < 2.8.0
Requires:	python3-pyflakes >= 2.3.0
Requires:	python3-pyflakes < 2.4.0

%description -n python3-flake8
The modular source code checker. It is a wrapper around these tools:
- PyFlakes
- pycodestyle
- Ned Batchelder's McCabe script

%description -n python3-flake8 -l pl.UTF-8
Modularne narzędzie do sprawdzania kodu źródłowego. Jest to opakowanie
dla narzędzi:
- PyFlakes
- pycodestyle
- skrypt McCabe autorstwa Neda Batcheldera

%package -n python-flake8-apidocs
Summary:	API documentation for Python flake8 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona flake8
Group:		Documentation

%description -n python-flake8-apidocs
API documentation for Python flake8 module.

%description -n python-flake8-apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona flake8.

%prep
%setup -q
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest -rw tests
%endif
%endif

%if %{with python3}
# don't require standalone mock
%{__sed} -i -e 's/import mock/from unittest import mock/' $(grep 'import mock' tests/ -rl)

%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -rw tests
%endif
%endif

%if %{with doc}
cd docs/source
PYTHONPATH=$(pwd)/../../src \
sphinx-build-3 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/flake8{,-2}
%py_postclean
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/flake8{,-3}
%endif

ln -s flake-%{!?with_python3:2}%{?with_python3:3} $RPM_BUILD_ROOT%{_bindir}/flake8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flake8

%if %{with python2}
%files -n python-flake8
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst
%attr(755,root,root) %{_bindir}/flake8-2
%{py_sitescriptdir}/flake8
%{py_sitescriptdir}/flake8-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-flake8
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst
%attr(755,root,root) %{_bindir}/flake8-3
%{py3_sitescriptdir}/flake8
%{py3_sitescriptdir}/flake8-%{version}-py*.egg-info
%endif

%if %{with doc}
%files -n python-flake8-apidocs
%defattr(644,root,root,755)
%doc docs/source/_build/html/{_modules,_static,internal,plugin-development,release-notes,user,*.html,*.js}
%endif

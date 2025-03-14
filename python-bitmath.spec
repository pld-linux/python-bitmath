#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	bitmath
Summary:	Module for representing file sizes with different prefix notations
Name:		python-%{module}
Version:	1.0.6
Release:	16
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/tbielawa/bitmath/archive/%{version}-1.tar.gz
# Source0-md5:	b589c9ceb7f518da043e089d519e8579
URL:		https://github.com/tbielawa/bitmath
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bitmath simplifies many facets of interacting with file sizes in
various units. Examples include: converting between SI and NIST prefix
units (GiB to kB), converting between units of the same type (SI to
SI, or NIST to NIST), basic arithmetic operations (subtracting 42KiB
from 50GiB), rich comparison operations (1024 Bytes == 1KiB), bitwise
operations (<<, >>, &, |, ^), and sorting.

In addition to the conversion and math operations, bitmath provides
human readable representations of values which are suitable for use in
interactive shells as well as larger scripts and applications.

%package -n python3-%{module}
Summary:	Module for representing file sizes with different prefix notations
Group:		Libraries/Python

%description -n python3-%{module}
bitmath simplifies many facets of interacting with file sizes in
various units. Examples include: converting between SI and NIST prefix
units (GiB to kB), converting between units of the same type (SI to
SI, or NIST to NIST), basic arithmetic operations (subtracting 42KiB
from 50GiB), rich comparison operations (1024 Bytes == 1KiB), bitwise
operations (<<, >>, &, |, ^), and sorting.

In addition to the conversion and math operations, bitmath provides
human readable representations of values which are suitable for use in
interactive shells as well as larger scripts and applications.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}-1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}*-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

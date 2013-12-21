Name:		sgml-common
Version:	0.6.3
Release:	40.0%{?dist}
Summary:	Common SGML catalog and DTD files
License:	GPL+
BuildArch:	noarch
URL:		http://www.w3.org/2003/entities/
Requires:	openjade

%description
The sgml-common package contains a collection of entities and DTDs
that are useful for processing SGML, but that don't need to be
included in multiple packages.  Sgml-common also includes an
up-to-date Open Catalog file.

%package	-n xml-common
Summary:	Common XML catalog and DTD files
Requires:	openjade

%description	-n xml-common
The xml-common is a subpackage of sgml-common which contains
a collection XML catalogs that are useful for processing XML,
but that don't need to be included in main package.

%prep

%build

%install

%files

%files		-n xml-common

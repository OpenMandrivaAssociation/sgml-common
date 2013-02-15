%define sgmlbase %{_datadir}/sgml

Summary:	Base ISO character entities and utilities for SGML and XML
Name:		sgml-common
Version:	0.6.3
Release:	21
Group:		Publishing
License:	GPLv3
Url:		http://www.w3.org/2003/entities/
Source0:	ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tar.bz2
Source1:	http://oasis-open.org/committees/docbook/xmlcharent/0.3/xmlcharent-0.3.tar.bz2
Source2:	xmlcharent-catalog.tar.bz2
# http://www.w3.org/2003/entities/iso8879/
Patch0:		sgml-common-0.6.3-umask.patch
Patch1:		sgml-common-xmldir.patch
Patch2:		sgml-common-quotes.patch
Patch3:		sgml-common-0.6.3-automake-fix.patch
BuildArch:	noarch

BuildRequires:	libxml2-utils >= 2.4.8-2
Requires:	coreutils
Requires:	grep
Requires:	libxml2-utils >= 2.4.8-2

%Description
The ISO standardization organization has normalized a set of characters
symbolic names ("character entities") used by SGML documents of many types.
There are character entities for latin languages, math symbols, greek,
cyrillic, etc. This package also includes very basic utilities to allow
SGML catalogs manipulation.

%prep
%setup -q
%setup -q -D -a 1
%setup -q -D -a 2
%patch0 -p1 -b .umask
%patch1 -p1 -b .xmldir
%patch2 -p1 -b .quotes
%patch3 -p1 -b .automake

autoreconf -fi

%build
%configure

%install
%makeinstall
# remove installed doc (added later in %files)
rm -rf %{buildroot}/usr/doc

# remove xml.dcl, it is now in openjade
rm -f %{buildroot}%{sgmlbase}/xml.dcl

# remove entities to install them later in /usr/share/sgml
# instead of /usr/share/xml
rm -rf %{buildroot}/usr/share/xml
mkdir %{buildroot}/etc/xml
mkdir %{buildroot}%{sgmlbase}/docbook
# Create an empty XML catalog.
XMLCATALOG=%{buildroot}/etc/xml/catalog
/usr/bin/xmlcatalog --noout --create $XMLCATALOG
# install common ISO entities character set
rm -rf %{buildroot}%{sgmlbase}/xml-iso-entities-8879.1986/
mkdir %{buildroot}%{sgmlbase}/xml-iso-entities-8879.1986/
install iso-*.ent %{buildroot}%{sgmlbase}/xml-iso-entities-8879.1986/
install catalog %{buildroot}%{sgmlbase}/xml-iso-entities-8879.1986/
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//ENTITIES DocBook XML" \
	"file://%{sgmlbase}/xml-iso-entities-8879.1986/catalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"ISO 8879:1986" \
	"file://%{sgmlbase}/xml-iso-entities-8879.1986/catalog" $XMLCATALOG
# Also create the common DocBook catalog
/usr/bin/xmlcatalog --noout --create \
	%{buildroot}%{sgmlbase}/docbook/xmlcatalog
# Now put the common DocBook entries
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file://%{sgmlbase}/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegateSystem" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{sgmlbase}/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegateURI" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{sgmlbase}/docbook/xmlcatalog" $XMLCATALOG

%files
%doc doc/HTML/*.html
%dir /etc/sgml
%config(noreplace) /etc/sgml/sgml.conf
%dir %{sgmlbase}
%dir %{sgmlbase}/sgml-iso-entities-8879.1986
%{sgmlbase}/sgml-iso-entities-8879.1986/*
%{_bindir}/sgmlwhich
%{_bindir}/install-catalog
%{_mandir}/man8/*

%dir /etc/xml
%config(noreplace) /etc/xml/catalog
%dir %{sgmlbase}/docbook
%config(noreplace) %{sgmlbase}/docbook/xmlcatalog
%dir %{sgmlbase}/xml-iso-entities-8879.1986/
%{sgmlbase}/xml-iso-entities-8879.1986/*


%define Name sgml-common
%define Version 0.6.3

Name:		%{Name}
Version:	%{Version}
Release:	%mkrel 16
Group       	: Publishing

Summary     	: Base ISO character entities and utilities for SGML and XML

License   	: GPL
URL         	: http://www.w3.org/2003/entities/


BuildRoot   	: %{_tmppath}/%{Name}-%{Version}

BuildArch	: noarch
Source0		: ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{Name}-%{Version}.tar.bz2
Source1		: http://oasis-open.org/committees/docbook/xmlcharent/0.3/xmlcharent-0.3.tar.bz2
Source2		: xmlcharent-catalog.tar.bz2
# http://www.w3.org/2003/entities/iso8879/
Patch0: sgml-common-0.6.3-umask.patch
Patch1: sgml-common-xmldir.patch
Patch2: sgml-common-quotes.patch
Patch3: sgml-common-0.6.3-automake-fix.patch

Requires: coreutils grep
Requires: libxml2-utils >= 2.4.8-2
BuildRequires: libxml2-utils >= 2.4.8-2
%if %{mdkversion} < 1010
BuildRequires: automake = 1.4
%endif

Obsoletes: xml-common
Provides: xml-common

%define sgmlbase %{_datadir}/sgml

%Description
The ISO standardization organization has normalized a set of characters
symbolic names ("character entities") used by SGML documents of many types.
There are character entities for latin languages, math symbols, greek,
cyrillic, etc. This package also includes very basic utilities to allow
SGML catalogs manipulation.

%Prep
%setup -q
%setup -q -D -a 1
%setup -q -D -a 2
%patch0 -p1 -b .umask
%patch1 -p1 -b .xmldir
%patch2 -p1 -b .quotes
%patch3 -p1 -b .automake

autoreconf -fi

%Build
%configure


%Install
rm -Rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT
%makeinstall
# remove installed doc (added later in %files)
rm -rf $DESTDIR/usr/doc

# remove xml.dcl, it is now in openjade
rm -f $RPM_BUILD_ROOT%{sgmlbase}/xml.dcl

# remove entities to install them later in /usr/share/sgml
# instead of /usr/share/xml
rm -rf $DESTDIR/usr/share/xml
mkdir $RPM_BUILD_ROOT/etc/xml
mkdir $RPM_BUILD_ROOT%{sgmlbase}/docbook
# Create an empty XML catalog.
XMLCATALOG=$RPM_BUILD_ROOT/etc/xml/catalog
/usr/bin/xmlcatalog --noout --create $XMLCATALOG
# install common ISO entities character set
rm -rf $RPM_BUILD_ROOT%{sgmlbase}/xml-iso-entities-8879.1986/
mkdir $RPM_BUILD_ROOT%{sgmlbase}/xml-iso-entities-8879.1986/
install iso-*.ent $RPM_BUILD_ROOT%{sgmlbase}/xml-iso-entities-8879.1986/
install catalog $RPM_BUILD_ROOT%{sgmlbase}/xml-iso-entities-8879.1986/
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//ENTITIES DocBook XML" \
	"file://%{sgmlbase}/xml-iso-entities-8879.1986/catalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"ISO 8879:1986" \
	"file://%{sgmlbase}/xml-iso-entities-8879.1986/catalog" $XMLCATALOG
# Also create the common DocBook catalog
/usr/bin/xmlcatalog --noout --create \
	$RPM_BUILD_ROOT%{sgmlbase}/docbook/xmlcatalog
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

%clean
rm -Rf $RPM_BUILD_ROOT

%Files
%defattr (-,root,root)
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

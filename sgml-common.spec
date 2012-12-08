%define Name sgml-common
%define Version 0.6.3

Name:		%{Name}
Version:	%{Version}
Release:	%mkrel 20
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


%changelog
* Mon Feb 20 2012 abf
- The release updated by ABF

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-19mdv2011.0
+ Revision: 669973
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-18mdv2011.0
+ Revision: 607534
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-17mdv2010.1
+ Revision: 520217
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.6.3-16mdv2010.0
+ Revision: 427085
- rebuild
- drop automake 1.4 dependency

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 0.6.3-15mdv2009.1
+ Revision: 366294
- rediff umask patch
- bunzip2 the patches

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.6.3-14mdv2009.0
+ Revision: 225437
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-13mdv2008.1
+ Revision: 179502
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 29 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-12mdv2008.0
+ Revision: 73375
- Import sgml-common




* Mon Sep  4 2006 Camille Begnis <camille@mandriva.com> 0.6.3-12mdv2007.0
- rebuild for 2007
- update URL
- clean specs

* Wed Aug 31 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.6.3-11mdk
- rebuild for 2006

* Fri Sep 17 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-10mdk
- force build with automake 1.4

* Fri May 14 2004 Camille Begnis <camille@mandrakesoft.com> 0.6.3-9mdk
- Use xmlcharent-0.3

* Fri Apr 25 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.6.3-8mdk
- xml.dcl is now in openjade
 
* Fri Jan 17 2003 Camille Begnis <camille@ke.mandrakesoft.com> 0.6.3-7mdk
- recompile against newer libs
- remove installed but not packaged files

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.6.3-6mdk
- requires s/(sh-|text|file)utils/coreutils/

* Thu Oct 31 2002  <camille@ke.mandrakesoft.com> 0.6.3-5mdk
- update symbolic links to automake-1.4 dir 

* Mon Jan 28 2002 Camille Begnis <camille@mandrakesoft.com> 0.6.3-4mdk
- Forgot to obsolete xml-common

* Thu Jan 24 2002 Camille Begnis <camille@mandrakesoft.com> 0.6.3-3mdk
- Buildrequires libxml2-utils

* Thu Jan 24 2002 Camille Begnis <camille@mandrakesoft.com> 0.6.3-2mdk
- use xmlcatalog from libxml-utils instead of install-catalog
- add support for XML catalogs as supported by libxml2 (xsltproc)

* Mon Aug 27 2001  <camille@ke.mandrakesoft.com> 0.6.3-1mdk
- 0.6.3

* Wed Mar 14 2001 Camille Begnis <camille@mandrakesoft.com> 0.2-4mdk
- Redirect install-catalog output to /dev/null

* Tue Feb 13 2001 Camille Begnis <camille@mandrakesoft.com> 0.2-3mdk
- move install-catalog.8.bz2 from man/en/man8 to man/man8

* Fri Jan 05 2001 Camille Begnis <camille@mandrakesoft.com> 0.2-2mdk
- add catalog management
- fix execute permissions

* Wed Aug 23 2000 Camille Begnis <camille@mandrakesoft.com> 0.2-1mdk
- 0.2
- adapt spec from Eric Bischoff <ebisch@cybercable.tm.fr>
- Pre-LSB compliance

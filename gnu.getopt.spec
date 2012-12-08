%define	section		free
%define gcj_support     1

Name:		gnu.getopt
Version:	1.0.13
Release:	%mkrel 1.3.8
Epoch:		0
Summary:        Java getopt implementation
License:        LGPL
Url:            http://www.urbanophile.com/arenn/hacking/download.html
Source0:        ftp://ftp.urbanophile.com/pub/arenn/software/sources/java-getopt-%{version}.tar.bz2
Obsoletes:      gnu-getopt < %{epoch}:%{version}-%{release}
Provides:       gnu-getopt = %{epoch}:%{version}-%{release}
BuildRequires:  ant
Group:          Development/Java
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The GNU Java getopt classes support short and long argument parsing in
a manner 100% compatible with the version of GNU getopt in glibc 2.0.6
with a mostly compatible programmer's interface as well. Note that this
is a port, not a new implementation. I am currently unaware of any bugs
in this software, but there certainly could be some lying about. I would
appreciate bug reports as well as hearing about positive experiences.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
# Aaron, where did you put my build script :-) ?
mv gnu/getopt/buildx.xml build.xml

%build
%ant jar javadoc

%install
%{__rm} -rf %{buildroot}

# jars
%__mkdir_p %{buildroot}%{_javadir}
%__install -m 644 build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %__ln_s ${jar} ${jar/-%{version}/}; done)
# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%__rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%__rm -f %{_javadocdir}/%{name}
%__ln_s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    %__rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc gnu/getopt/COPYING.LIB gnu/getopt/README
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}



%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.13-1.3.6mdv2011.0
+ Revision: 664896
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.13-1.3.5mdv2011.0
+ Revision: 605483
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.13-1.3.4mdv2010.1
+ Revision: 522739
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.0.13-1.3.3mdv2010.0
+ Revision: 425015
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.0.13-1.3.2mdv2009.0
+ Revision: 136454
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0.13-1.3.2mdv2008.1
+ Revision: 120888
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0.13-1.3.1mdv2008.0
+ Revision: 87382
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Fri Sep 14 2007 David Walluck <walluck@mandriva.org> 0:1.0.13-1.3.0mdv2008.0
+ Revision: 85488
- Provide gnu-getopt for JPackage compatibility

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.0.13-1.3mdv2008.0
+ Revision: 82838
- update to new version


* Wed Mar 14 2007 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2007-03-14 17:43:22 (143736)
- rebuild for 2007.1
- Import gnu.getopt

* Sun Sep 03 2006 David Walluck <walluck@mandriva.org> 0:1.0.13-1.1mdv2007.0
- aot-compile
- clean %%{buildroot} in %%install

* Sun Sep 03 2006 David Walluck <walluck@mandriva.org> 0:1.0.13-1mdv2007.0
* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.0.10-1.1mdk
- release

* Tue Dec 07 2004 David Walluck <david@jpackage.org> 0:1.0.10-1jpp
- 1.0.10

* Tue Aug 24 2004 Ralph Apel <r.apel at r-apel.de> 0:1.0.9-5jpp
- Build with ant-1.6.2


%define	section		free
%define gcj_support     1

Name:		gnu.getopt
Version:	1.0.13
Release:	%mkrel 1.3.2
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
%__cp -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}

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


%define	section		free
%define gcj_support     0

Summary:        Java getopt implementation
Name:		gnu.getopt
Version:	1.0.14
Release:	2
License:        LGPLv2
Group:          Development/Java
Url:            http://www.urbanophile.com/arenn/hacking/download.html
Source0:        ftp://ftp.urbanophile.com/pub/arenn/software/sources/java-getopt-%{version}.tar.bz2
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRequires:	java-rpmbuild >= 0:1.5
Provides:       gnu-getopt = %{EVRD}

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
# jars
mkdir -p %{buildroot}%{_javadir}
install -m 644 build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} ${jar/-%{version}/}; done)
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%doc gnu/getopt/COPYING.LIB gnu/getopt/README
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}


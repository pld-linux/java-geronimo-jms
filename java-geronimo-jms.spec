#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with		tests		# don't build and run tests

%define		srcname		geronimo-jms
%define		spec_name	%{srcname}_1.1_spec
Summary:	J2EE JMS v1.1 API
Name:		java-geronimo-jms
Version:	1.1.1
Release:	2
License:	ASL 2.0
Group:		Libraries/Java
URL:		http://geronimo.apache.org/
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/%{spec_name}-%{version}/
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/geronimo-jms/%{spec_name}-%{version}.tar.bz/987d1e6b659c066648bc61cf9e8ea201/%{spec_name}-%{version}.tar.bz
# Source0-md5:	987d1e6b659c066648bc61cf9e8ea201
# Remove unavailable dependencies
Patch0:		geronimo-jms-1.1-api-remove-mockobjects.patch
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Provides:	java(jms) = %{version}-%{release}
Provides:	jms = %{version}-%{release}
Obsoletes:	geronimo-jms < 1.1.1-0.1
Obsoletes:	geronimo-specs <= 1.0-3.3
Obsoletes:	geronimo-specs-compat <= 1.0-3.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Java Message Service (JMS) API is a messaging standard that allows
application components based on the Java 2 Platform, Enterprise
Edition (J2EE) to create, send, receive, and read messages. It enables
distributed communication that is loosely coupled, reliable, and
asynchronous.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q -n %{spec_name}-%{version}
%patch -P0 -p1

%build
# do what 'mvn package' would
install -d target/{classes,test-classes,docs/apidocs}
%javac -d target/classes -encoding UTF-8 $(find src/main -type f -name "*.java")

%if %{with tests}
%javac -d target/test-classes -encoding UTF-8 $(find src/test -type f -name "*.java")
%endif

%jar -cvf target/%{spec_name}-%{version}.jar -C target/classes .

%javadoc -d target/docs/apidocs $(find src/main -name '*.java')

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -p target/%{spec_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# Also provide compat symlinks
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{spec_name}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jms.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar
%{_javadir}/%{spec_name}.jar
%{_javadir}/jms.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

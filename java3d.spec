Name:		java3d
Group:		Graphics
Summary:	Master project for Java 3D projects
Version:	1.5.2
# And some restrictions like Sun and others IP/patents, US embargos, etc
License:	BSD like and GPLv2+
Release:	2

# register an user at https://www.dev.java.net
# mkdir java3d-1.5.2
# cd java3d-1.5.2
# svn checkout https://vecmath.dev.java.net/svn/vecmath/trunk vecmath
# svn checkout https://j3d-core.dev.java.net/svn/j3d-core/trunk j3d-core
# svn checkout https://j3d-core-utils.dev.java.net/svn/j3d-core-utils/trunk j3d-core-utils
# find vecmath -name .svn -exec rm -fr {} \;
# find j3d-core -name .svn -exec rm -fr {} \;
# find j3d-core-utils -name .svn -exec rm -fr {} \;
# cd ..
# tar jcf java3d-1.5.2.tar.bz2 java3d-1.5.2
Source0:	java3d-1.5.2.tar.bz2
# http://wiki.java.net/bin/view/Javadesktop/Java3DFAQ
URL:		https://java3d.dev.java.net
Patch0:		06_java-compat.patch

#-----------------------------------------------------------------------
BuildRequires:  ant
BuildRequires:	ant-apache-bcel
BuildRequires:	ant-nodeps
BuildRequires:	crimson
BuildRequires:	pkgconfig(gl)
BuildRequires:  java-rpmbuild
BuildRequires:	jpackage-utils
BuildRequires:  jpeg-devel
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	pkgconfig(xt)

#-----------------------------------------------------------------------
%description
This is the parent project for all Java 3DTM-related sub-projects on java.net.
These sub-projects include: j3d-core (the core 3D API), vecmath (the 3D vector
math package), and j3d-core-utils (the 3D core utilities), among others. See
the complete list of sub-projects at the bottom of this page.

Note that there is no source code in this parent project; source code files for
the various 3D sub-projects are in the sub-projects themselves.

#-----------------------------------------------------------------------
%package devel
Summary:	Development files for %{name}
Group:		Development/Other

%description devel
Development files and headers for %{name}.

#-----------------------------------------------------------------------
%package javadoc
Summary:	Documentation files for %{name}
Group:		Development/Other

%description javadoc
Documentation files and headers for %{name}.

#-----------------------------------------------------------------------
%prep
%setup -q
%apply_patches

#-----------------------------------------------------------------------
%define ant	JAVA_HOME=%{java_home} ant

%build
pushd vecmath
    %ant jar
    %ant docs
popd

pushd j3d-core
    %ant compile
    %ant jar
    %ant docs
popd

#-----------------------------------------------------------------------
%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_javadir}
mkdir -p %{buildroot}%{_javadocdir}/{vecmath,j3d-core}
mkdir -p %{buildroot}%{_datadir}/java3d/{vecmath,j3d}

pushd vecmath
    install -m644 build/opt/lib/ext/vecmath.jar %{buildroot}%{_javadir}
    cp -fa docs/* %{buildroot}%{_javadocdir}/vecmath
    cp -far build/javadocs/* %{buildroot}%{_javadocdir}/vecmath
    cp -far build/opt/gen %{buildroot}%{_datadir}/java3d/vecmath
    cp -far build/opt/classes %{buildroot}%{_datadir}/java3d/vecmath
popd

pushd j3d-core
    install -m755 build/linux-*/opt/lib/*/libj3dcore-ogl.so %{buildroot}%{_libdir}
    install -m644 build/linux-*/opt/lib/ext/{j3dcore,j3dutils}.jar %{buildroot}%{_javadir}
    cp -fa build/linux-*/javadocs/* %{buildroot}%{_javadocdir}/j3d-core
    cp -far build/linux-*/opt/gen %{buildroot}%{_datadir}/java3d/j3d
    cp -far build/linux-*/opt/classes %{buildroot}%{_datadir}/java3d/j3d
popd

#-----------------------------------------------------------------------
%files
%{_javadir}/*
%{_libdir}/*.so

%files	devel
%dir %{_datadir}/java3d
%{_datadir}/java3d/*

%files	javadoc
%dir %{_javadocdir}/vecmath
%{_javadocdir}/vecmath/*
%dir %{_javadocdir}/j3d-core
%{_javadocdir}/j3d-core/*

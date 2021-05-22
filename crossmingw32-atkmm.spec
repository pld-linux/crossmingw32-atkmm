Summary:	A C++ interface for atk library - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki atk - wersja skrośna MinGW32
Name:		crossmingw32-atkmm
Version:	2.28.2
Release:	1
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	https://download.gnome.org/sources/atkmm/2.28/atkmm-%{version}.tar.xz
# Source0-md5:	c1dc581b9cf14a8f3cd088a7563d0d3e
URL:		https://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	crossmingw32-atk >= 2.18.0
BuildRequires:	crossmingw32-gcc-c++ >= 1:4.7
BuildRequires:	crossmingw32-glibmm >= 2.46.2
# for gmmproc tools
BuildRequires:	glibmm-devel >= 2.46.2
BuildRequires:	libtool >= 2:2.0
BuildRequires:	mm-common >= 0.9.10
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-atk >= 2.18.0
Requires:	crossmingw32-gcc-c++ >= 1:4.7
Requires:	crossmingw32-glibmm >= 2.46.2
Provides:	crossmingw32-gtkmm-atk
Obsoletes:	crossmingw32-gtkmm-atk < 2.22.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%define		_ssp_cflags		%{nil}
%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c		-f[-a-z0-9=]*

%description
A C++ interface for atk library - cross MinGW32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki atk - wersja skrośna MinGW32.

%package static
Summary:	Static atkmm library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka atkmm (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	crossmingw32-gtkmm-atk-static
Obsoletes:	crossmingw32-gtkmm-atk-static < 2.22.0

%description static
Static atkmm library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka atkmm (wersja skrośna MinGW32).

%package dll
Summary:	DLL atkmm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL atkmm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-atk-dll >= 2.18.0
Requires:	crossmingw32-glibmm-dll >= 2.46.2
Requires:	wine
Provides:	crossmingw32-gtkmm-atk-dll
Obsoletes:	crossmingw32-gtkmm-atk-dll < 2.22.0

%description dll
DLL atkmm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL atkmm dla Windows.

%prep
%setup -q -n atkmm-%{version}

%build
# use host gmmprocdir (before changing PKG_CONFIG_LIBDIR to cross target)
GMMPROC_DIR=$(pkg-config --variable=gmmprocdir glibmm-2.4)
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig:%{_npkgconfigdir}
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
# std-threads required by glibmm requires at least WinXP API
CPPFLAGS="%{rpmcppflags} -DWINVER=0x0501"
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-documentation \
	--enable-maintainer-mode \
	--disable-silent-rules \
	--enable-static

%{__make} \
	GMMPROC_DIR="$GMMPROC_DIR"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libatkmm-*.la

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libatkmm-1.6.dll.a
%{_libdir}/atkmm-1.6
%{_includedir}/atkmm-1.6
%{_pkgconfigdir}/atkmm-1.6.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libatkmm-1.6.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libatkmm-1.6-1.dll

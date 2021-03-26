# slowmovideo
%global gitdate 20210320
%global commit0 279026ad91e034e49c712e8b7a02b3e109f1af2d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

# libsvflow
%global commit1 7c31a0bf9467e774442473e8b951b09fe6eb1b9f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# v3d-flow-builder
%global commit2 e9d235178fe90e5ce6f53a18def4638eff4dd921
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})


Name:           slowmovideo
Version:        0.6
Release:	7%{gver}%{?dist}
Summary:        Video slow motion effect via interpolation
License:        GPLv3+
Group:          Productivity/Multimedia/Video/Editors and Convertors
URL:            http://slowmovideo.granjow.net/
Source0:  	https://github.com/slowmoVideo/slowmoVideo/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:  	https://github.com/slowmoVideo/libsvflow/archive/%{commit1}.tar.gz#/libsvflow-%{shortcommit1}.tar.gz
Source2:  	https://github.com/slowmoVideo/v3d-flow-builder/archive/%{commit2}.tar.gz#/v3d-flow-builder-%{shortcommit2}.tar.gz

Patch1:         slowmoVideo-desktop.patch
Patch2:		headers_fix.patch
Patch3:		OpenCV4_compile.patch
BuildRequires:  ImageMagick
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  freeglut-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(opencv)
BuildRequires:  opencv-static
BuildRequires:  pkgconfig(sdl)

# v3d-flow-builder
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib)

Requires:       ffmpeg
Requires:	glslang

%description
Is an OpenSource program that creates slow-motion videos from your footage.

But it does not simply make your videos play at 0.01× speed. You can
smoothly slow down and speed up your footage, optionally with motion blur.

How does slow motion work? slowmoVideo tries to find out where pixels move
in the video (this information is called Optical Flow), and then uses this
information to calculate the additional frames between the ones recorded by
your camera.

%prep
%setup -n slowmoVideo-%{commit0} -a1
%patch1 -p1
%patch3 -p1
rm -rf src/lib/libsvflow && mv -f libsvflow-%{commit1} src/lib/libsvflow 

#------------------------------------------
%setup -T -D -n slowmoVideo-%{commit0} -a2 
%patch2 -p1 -d v3d-flow-builder-%{commit2}
rm -rf v3d-flow-builder-%{commit2}/src/lib/libsvflow && tar -xf %{S:1} -C $PWD/v3d-flow-builder-%{commit2}/src/lib/
mv -f  $PWD/v3d-flow-builder-%{commit2}/src/lib/libsvflow-%{commit1}  $PWD/v3d-flow-builder-%{commit2}/src/lib/libsvflow

%build

pushd v3d-flow-builder-%{commit2}
%cmake \
	-DUSE_DBUS=ON \
	-DDISABLE_INCLUDE_SOURCE=ON \
	-DENABLE_TESTS=OFF \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-Wno-dev
  
%cmake_build
popd

%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DENABLE_TESTS=OFF \
	-Wno-dev
	
%cmake_build

%install

pushd v3d-flow-builder-%{commit2}
%cmake_install
popd


%cmake_install
for s in 16 32 48 64 96 128 192 256 512; do
   mkdir -pv %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
   convert -strip -scale ${s}x${s} src/slowmoUI/res/AppIcon.png %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/slowmoUI.png
done

%files
%{_bindir}/slowmoFlowEdit
%{_bindir}/slowmoInterpolate
%{_bindir}/slowmoRenderer
%{_bindir}/slowmoUI
%{_bindir}/slowmoVideoInfo
%{_bindir}/slowmoVisualizeFlow
%{_bindir}/slowmoFlowBuilder
%{_datadir}/applications/slowmoUI.desktop
%{_datadir}/icons/hicolor/*/apps/slowmoUI.png

%changelog

* Sat Mar 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.6-7.git279026ad
- Updated to 0.6-7.git279026ad and reviving the dead

* Fri Mar 20 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.4-1.20150320git3626dfe
- Initial build

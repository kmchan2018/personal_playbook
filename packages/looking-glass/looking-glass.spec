%global lg_version B6

Name:           looking-glass
Version:        0~%{lg_version}
Release:        1%{?dist}
Summary:        Extremely Low Latency KVM Frame Relay Implementation
License:        GPL-2.0-or-later and MIT and Zlib
URL:            https://looking-glass.io/
Source0:        https://github.com/gnif/LookingGlass/archive/refs/tags/%{lg_version}.tar.gz

#
# While the main program is licensed under GPL, it also statically
# links cimgui and nanosvg, which is licensed under MIT and Zlib
# respectively.
#

Requires:       dejavu-sans-mono-fonts

BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libXrandr-devel
BuildRequires:  make
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hogweed)
BuildRequires:  pkgconfig(libdecor-0)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(spice-protocol)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xpresent)
BuildRequires:  pkgconfig(xscrnsaver)

#
# CMake files in the source tree detects dependencies using pkgconfig and
# therefore they should be listed as pkgconfig(foo). Below is a list of
# such packages:
#
# client:                        fontconfig samplerate
# client/audiodevs/pipewire:     libpipewire-0.3
# client/audiodevs/pulse:        libpulse
# client/displayservers/Wayland: wayland-client wayland-cursor xkbcommon libdecor-0
# client/displayservers/X11:     x11 xi xfixes xscrnsaver xinerama xcursor xpresent xkbcommon
# client/renderers/EGL:          egl gl wayland-egl
# client/renderers/OpenGL:       gl
# repos/PureSpice:               spice-protocol nettle hogweed
#
# For some reason, pkgconfig(xrandr) is not listed in the CMake files but
# are required to compile the program. Hence a separate build requires
# entry for libXrandr-devel.
#

Provides:       bundled(LGMP)
Provides:       bundled(PureSpice)
Provides:       bundled(cimgui)
Provides:       bundled(nanosvg)

%description
Looking Glass is an open source application that allows the use of a KVM
(Kernel-based Virtual Machine) configured for VGA PCI Pass-through without
an attached physical monitor, keyboard or mouse.

%prep
%autosetup -n looking-glass-%{lg_version} -p1

%build
mkdir -p client/build
cd client/build
%cmake -DENABLE_LIBDECOR=ON -DENABLE_BACKTRACE=OFF ..
%cmake_build

%install
cd client/build
%cmake_install

%files
%license LICENSE
%doc AUTHORS CONTRIBUTORS README.md
%{_bindir}/looking-glass-client

%changelog
* Thu Feb 16 2023 Chan Kwun Man <kmchan3@gmail.com> - 0~B6-1
- Initial package

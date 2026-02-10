%define _disable_source_fetch 0
%global _build_id_links none

Name: scx-manager
Version: 1.15.9
Release: 1%{?dist}
Summary: Simple GUI for managing sched-ext schedulers via scx_loader

License:        GPL-3.0
URL:            https://github.com/cachyos/scx-manager
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  make
BuildRequires:  ninja-build
BuildRequires:  systemd-devel
BuildRequires:  fmt-devel
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang >= 17
BuildRequires:  llvm >= 17
BuildRequires:  lld >= 17
BuildRequires:  qt6-qttools-devel
BuildRequires:  cmake
Requires:       scx-scheds
Requires:       scx-tools

%description
Simple GUI for managing sched-ext schedulers via scx_loader.

%prep
%autosetup

%build
%{cmake} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} .
%cmake_build

%install
%cmake_install

%files
%{_bindir}/scx-manager
%{_includedir}/scx-manager/schedext-window.hpp
%{_libdir}/cmake/scxctl-ui/scxctl-ui-config.cmake
%{_libdir}/cmake/scxctl-ui/scxctl-ui-targets.cmake
%{_libdir}/cmake/scxctl-ui/scxctl-ui-config-version.cmake
%{_libdir}/cmake/scxctl-ui/scxctl-ui-targets-release.cmake
%{_libdir}/libscxctl-ui.so
%{_libdir}/libscxctl-ui.so.1
%{_libdir}/libscxctl-ui.so.%{version}
%{_prefix}/share/applications/org.cachyos.scx-manager.desktop
%{_prefix}/share/icons/hicolor/scalable/apps/org.cachyos.scx-manager.png


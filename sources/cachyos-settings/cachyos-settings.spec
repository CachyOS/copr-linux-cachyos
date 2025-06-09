%define _disable_source_fetch 0
%define debug_package %{nil}

Name:           cachyos-settings
Release:        1%{?dist}
Version:        1.2.5
Summary:        CachyOS-Settings ported to Fedora
License:        GPL-3.0-or-later
URL:            https://github.com/CachyOS/CachyOS-Settings
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

Requires:       zram-generator
Requires:       lua-luv
Provides:       zram-generator-defaults
Provides:       kerver
Conflicts:      zram-generator-defaults
Obsoletes:      bore-sysctl

%description
    CachyOS-Settings for Fedora based systems

%prep
    %autosetup -p1 -n CachyOS-Settings-%{version}

%install
    install -d %{buildroot}/%{_bindir}
    install -d %{buildroot}/%{_prefix}/lib
    cp %{_builddir}/CachyOS-Settings-%{version}/usr/{bin,lib} %{buildroot}/%{_prefix} -r
    mv %{buildroot}/%{_prefix}/lib/modprobe.d/nvidia.conf %{buildroot}/%{_prefix}/lib/modprobe.d/nvidia_cachyos.conf
    chmod +x %{buildroot}/%{_bindir}/*

%files
    %{_bindir}/*
    %{_prefix}/lib/*

%changelog
%autochangelog






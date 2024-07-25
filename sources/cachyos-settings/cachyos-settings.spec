%define _disable_source_fetch 0
%define debug_package %{nil}

Name:           cachyos-settings
Release:        3%{?dist}
Version:        1.0.7
Summary:        CachyOS-Settings ported to Fedora
License:        GPLv3
URL:            https://github.com/CachyOS/CachyOS-Settings
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
BuildRequires:  git

Requires: zram-generator

Provides: zram-generator-defaults
Provides: kerver
Obsoletes: zram-generator-defaults
Obsoletes: bore-sysctl

%description
CachyOS-Settings for Fedora based systems

%prep
%autosetup -n CachyOS-Settings-%{version}

%if 0%{?fedora} < 41
git init
git remote add origin https://github.com/CachyOS/CachyOS-Settings
git fetch origin
git checkout %{version} -b remove_ksm -f
# Revert systemd ksm
git revert d4db4b7 --no-commit
%endif

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






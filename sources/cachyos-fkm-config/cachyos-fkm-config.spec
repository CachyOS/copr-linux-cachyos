%define _disable_source_fetch 0

Name:          cachyos-fkm-config
Version:       1.0
Release:       1%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       Config files to enable coprs/bieszczaders/kernel-cachyos in fedora-kernel-manager.


URL:            https://github.com/sirlucjan/copr-linux-cachyos
Source0:        https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/cachyos-fkm-config/kernel-cachyos.json
Source1:        https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/cachyos-fkm-config/kernel-cachyos-init.sh
Source2:        https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/cachyos-fkm-config/fkm.kernel.cachyos.init.policy
Source3:        https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/cachyos-fkm-config/99-fkm.kernel.cachyos.init.rules

Requires:   fedora-kernel-manager

%description
Config files to enable coprs/bieszczaders/kernel-cachyos in fedora-kernel-manager.

%install
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/fedora-kernel-manager/kernel_branches/
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/fedora-kernel-manager/scripts
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/polkit-1/actions/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/polkit-1/rules.d/
cp %{SOURCE0} $RPM_BUILD_ROOT/%{_prefix}/lib/fedora-kernel-manager/kernel_branches/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_prefix}/lib/fedora-kernel-manager/scripts/
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/polkit-1/actions/
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/polkit-1/rules.d/
chmod 755 $RPM_BUILD_ROOT/%{_prefix}/lib/fedora-kernel-manager/scripts/kernel-cachyos-init.sh

%files
%{_prefix}/lib/fedora-kernel-manager/kernel_branches/kernel-cachyos.json
%{_prefix}/lib/fedora-kernel-manager/scripts/kernel-cachyos-init.sh
%{_datadir}/polkit-1/actions/fkm.kernel.cachyos.init.policy
%{_datadir}/polkit-1/rules.d/99-fkm.kernel.cachyos.init.rules
%define _disable_source_fetch 0
%define debug_package %{nil}

Name:           cachyos-ksm-settings
Release:        3%{?dist}
Version:        1
Summary:        Package for easy configuration of KSM via systemd
URL:            https://github.com/CachyOS/CachyOS-PKGBUILDS
License:        Unknown

Source0:        %{url}/raw/refs/heads/master/%{name}/10-enable-ksm-by-default.conf
Source1:        %{url}/raw/refs/heads/master/%{name}/10-systemd-ksm.conf
Source2:        %{url}/raw/refs/heads/master/%{name}/ksmctl
Source3:        %{url}/raw/refs/heads/master/%{name}/ksmstats

Conflicts:      cachyos-settings < 1.1.8
Conflicts:      uksmd
Obsoletes:      uksmd
Requires:       systemd >= 256

%description
    This package provides easy configuration of kernel same-page merging via systemd.

%install
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/gdm.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/sddm.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/lightdm.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/ly.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/user@.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE1} "%{buildroot}/%{_prefix}/lib/systemd/system/getty@.service.d/10-ksm.conf"
    install -Dm644 %{SOURCE0} "%{buildroot}/%{_prefix}/lib/tmpfiles.d/10-enable-ksm-by-default.conf"
    install -Dm755 %{SOURCE2} "%{buildroot}/%{_bindir}/ksmctl"
    install -Dm755 %{SOURCE3} "%{buildroot}/%{_bindir}/ksmstats"

%files
    %{_bindir}/*
    %{_prefix}/lib/*

%changelog
%autochangelog




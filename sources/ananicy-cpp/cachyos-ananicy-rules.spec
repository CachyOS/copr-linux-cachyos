%global commit c6153c9e909475bbb08b4e56af152179ff7f171f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define _disable_source_fetch 0

Name:           cachyos-ananicy-rules
Version:        20240727.r%{shortcommit}
Release:        1%{?dist}
Summary:        List of rules used to assign specific nice values to specific processes

License:        GPL=3.0
URL:            https://github.com/CachyOS/ananicy-rules
Source0:        %{URL}/archive/%{commit}/ananicy-rules-%{commit}.tar.gz

Requires: ananicy-cpp
Obsoletes: ananicy-cpp-rules < %{version}-%{release}
Provides:  ananicy-cpp-rules = %{version}-%{release}

%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%description
List of rules used to assign specific nice values to specific processes

%prep
%autosetup -n ananicy-rules-%{commit}

%install
install -d %{buildroot}/etc/ananicy.d
cp %{_builddir}/ananicy-rules-%{commit}/00-default %{buildroot}/etc/ananicy.d/ -r
cp %{_builddir}/ananicy-rules-%{commit}/00-cgroups.cgroups %{buildroot}/etc/ananicy.d/ -r
cp %{_builddir}/ananicy-rules-%{commit}/00-types.types %{buildroot}/etc/ananicy.d/ -r
cp %{_builddir}/ananicy-rules-%{commit}/ananicy.conf %{buildroot}/etc/ananicy.d/ -r

%files
%defattr(-,root,root,-)
/etc/ananicy.d/*

%changelog
%autochangelog

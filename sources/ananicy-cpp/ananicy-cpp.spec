### The author of ananicy-cpp
# Vladislav Nepogodin <nepogodin.vlad@gmail.com>
### The port maintainer for Fedora:
# bieszczaders <zbyszek@linux.pl>
# https://copr.fedorainfracloud.org/coprs/bieszczaders/


%define _disable_source_fetch 0

Name:           ananicy-cpp
Release:        13%{?dist}
Version:	    1.1.1
Summary:        Rewrite of ananicy in c++ for lower cpu and memory usage
License:        GPLv3
URL:            https://gitlab.com/ananicy-cpp/ananicy-cpp
Source0:        %{url}/-/archive/v%{version}/ananicy-cpp-v%{version}.tar.gz
Patch0:         https://raw.githubusercontent.com/CachyOS/copr-linux-cachyos/refs/heads/ananicy-buildfix/sources/patches/ananicy-cpp-glibc-2.41.patch
%if 0%{?fedora} >= 44
Patch1:         https://raw.githubusercontent.com/CachyOS/copr-linux-cachyos/refs/heads/ananicy-buildfix/sources/patches/ananicy-cpp-gcc-15-weak-ptr.patch
Patch2:         https://raw.githubusercontent.com/CachyOS/copr-linux-cachyos/refs/heads/ananicy-buildfix/sources/patches/ananicy-cpp-gcc-15-maybe-unused.patch
Patch3:         https://raw.githubusercontent.com/CachyOS/copr-linux-cachyos/refs/heads/ananicy-buildfix/sources/patches/ananicy-cpp-gcc-15-includes.patch
Patch4:         https://raw.githubusercontent.com/CachyOS/copr-linux-cachyos/refs/heads/ananicy-buildfix/sources/patches/ananicy-cpp-gcc-15-bpf-prog.patch
%endif

ExcludeArch:    s390x i686 ppc64le

BuildRequires:  bpftool
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  fmt-devel
BuildRequires:  json-devel
BuildRequires:  libbpf-devel
BuildRequires:  ninja-build
BuildRequires:  spdlog-devel
BuildRequires:  systemd-devel

Requires:       elfutils-libelf
Requires:       fmt
Requires:       glibc
Requires:       libbpf
Requires:       spdlog
Requires:       systemd
Requires:       systemd-libs
Requires:       zlib-ng-compat

Recommends:     cachyos-ananicy-rules


%description
Rewrite of ananicy in c++ for lower cpu and memory usage


%prep
%autosetup -n ananicy-cpp-v%{version} -p1

%build
%cmake \
    -GNinja \
    -DENABLE_SYSTEMD=ON \
    -DUSE_BPF_PROC_IMPL=ON \
    -DBPF_BUILD_LIBBPF=OFF \
    -DUSE_EXTERNAL_FMTLIB=ON \
    -DUSE_EXTERNAL_JSON=ON \
    -DUSE_EXTERNAL_SPDLOG=ON \
    -DVERSION=%{version}
%cmake_build --target %{name}

%install
%cmake_install --component Runtime

%posttrans
systemctl enable --now ananicy-cpp

%preun
systemctl disable --now ananicy-cpp


%files
%license LICENSE
%doc README.md
%{_bindir}/ananicy-cpp
%{_unitdir}/ananicy-cpp.service

%changelog
%autochangelog/*

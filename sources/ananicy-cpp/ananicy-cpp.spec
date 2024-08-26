### The author of ananicy-cpp
# Vladislav Nepogodin <nepogodin.vlad@gmail.com>
### The port maintainer for Fedora:
# bieszczaders <zbyszek@linux.pl>
# https://copr.fedorainfracloud.org/coprs/bieszczaders/


%define _disable_source_fetch 0

Name:           ananicy-cpp
Release:        9%{?dist}
Version:	    1.1.1
Summary:        Rewrite of ananicy in c++ for lower cpu and memory usage
License:        GPLv3
URL:            https://gitlab.com/ananicy-cpp/ananicy-cpp
Source0:        %{url}/-/archive/v%{version}/ananicy-cpp-v%{version}.tar.gz

ExcludeArch:    s390x i686 ppc64le

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  zlib-devel
BuildRequires:  git
BuildRequires:  bpftool
BuildRequires:  libbpf-devel
BuildRequires:  elfutils-libelf
BuildRequires:  llvm
BuildRequires:  clang
Requires:	ananicy-cpp-rules

%description
Rewrite of ananicy in c++ for lower cpu and memory usage


%prep
%autosetup -n ananicy-cpp-v%{version}

%build
%cmake \
    -GNinja \
    -DENABLE_SYSTEMD=ON \
    -DUSE_BPF_PROC_IMPL=OFF \
    -DBPF_BUILD_LIBBPF=OFF \
    -DENABLE_ANANICY_TESTS=ON \
    -DBUILD_SHARED_LIBS=OFF \
    -DVERSION=%{version}
%ninja_build -C %{_vpath_builddir}

%install
%ninja_install -C %{_vpath_builddir}



%check
./%{_vpath_builddir}/src/tests/test-core
./%{_vpath_builddir}/src/tests/test-utility --test-case-exclude="Process Info"

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

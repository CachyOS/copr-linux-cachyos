%global _default_patch_fuzz 2
%global commitdate 20260218
%global commit 30b4540650f0283136c875efb4cd449686a87995
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define _disable_source_fetch 0

Name:           scx-tools-git
Version:        1.0.20.%{commitdate}.git.%{shortcommit}
Release:        1%{?dist}
Summary:        Sched_ext Tools

License:        GPL=2.0
URL:            https://github.com/sched-ext/scx-loader
Source0:        %{URL}/archive/%{commit}/scx-loader-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  python
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang >= 17
BuildRequires:  llvm >= 17
BuildRequires:  lld >= 17
BuildRequires:  systemd
BuildRequires:  bpftool
BuildRequires:  libseccomp-devel
Requires:  scx-scheds
Obsoletes: scxctl = 0.3.4
Provides: scxctl = %{version}
Provides: scx-tools = %{version}
Conflicts: scx-tools

%description
scx_loader: A DBUS Interface for Managing sched_ext Schedulers

%prep
%autosetup -p1 -n scx-loader-%{commit}

%build
export CARGO_HOME=%{_builddir}/.cargo
cargo fetch --locked
cargo build --release --frozen --all-features --workspace

%install

# Install all built executables (skip .so and .d files)
find target/release \
    -maxdepth 1 -type f -executable ! -name '*.so' ! -name 'xtask' \
    -exec install -Dm755 -t %{buildroot}%{_bindir} {} +

# Install runtime assets via xtask
# (systemd units, D-Bus services, configs, sample files)
./target/release/xtask install --destdir %{buildroot}

%files

# Binaries
%{_bindir}/*

# Systemd service
%{_unitdir}/scx_loader.service

# DBus service and configuration
%{_datadir}/dbus-1/system-services/org.scx.Loader.service
%{_datadir}/dbus-1/system.d/org.scx.Loader.conf
%{_datadir}/dbus-1/interfaces/org.scx.Loader.xml

# Polkit authorization policy for scx-loader
%{_datadir}/polkit-1/actions/org.scx.Loader.policy

# Configuration files
%{_datadir}/scx_loader/config.toml

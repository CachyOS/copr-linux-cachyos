%define _disable_source_fetch 0

Name:           scx-tools
Version:        1.0.18
Release:        2%{?dist}
Summary:        Sched_ext Tools

License:        GPL=2.0
URL:            https://github.com/sched-ext/scx-loader
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

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

%description
scx_loader: A DBUS Interface for Managing sched_ext Schedulers

%prep
%autosetup -n scx-loader-%{version}

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

# Polkit authorization policy for scx-loader
%{_datadir}/polkit-1/actions/org.scx.Loader.policy

# Configuration files
%{_datadir}/scx_loader/config.toml

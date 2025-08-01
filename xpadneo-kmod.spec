%global commit0 a16acb03e7be191d47ebfbc8ca1d5223422dac3e
%global date 20250705
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:           xpadneo-kmod
Version:        0.9.7%{!?tag:^%{date}git%{shortcommit0}}
Release:        2%{?dist}
Summary:        Advanced Linux Driver for Xbox One Wireless Gamepad
License:        GPLv3
URL:            https://atar-axis.github.io/xpadneo

%if 0%{?tag:1}
Source0:        https://github.com/atar-axis/xpadneo/archive/v%{version}.tar.gz#/xpadneo-%{version}.tar.gz
%else
Source0:        https://github.com/atar-axis/xpadneo/archive/%{commit0}.tar.gz#/xpadneo-%{shortcommit0}.tar.gz
%endif


# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Advanced Linux Driver for Xbox One Wireless Gamepad.

%prep
# Rrror out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%if 0%{?tag:1}
%autosetup -p1 -n xpadneo-%{version}
%else
%autosetup -p1 -n xpadneo-%{commit0}
%endif

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr hid-xpadneo/src/* _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd) VERSION="v%{version}" modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Fri Aug 01 2025 Simone Caronni <negativo17@gmail.com> - 0.9.7^20250705gita16acb0-2
- Update to latest snapshot.

* Wed Dec 25 2024 Simone Caronni <negativo17@gmail.com> - 0.9.7-1
- Update to 0.9.7.

* Fri Dec 06 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6^20241206git45dac5d-6
- Update to latest snapshot.

* Fri Nov 29 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6^20241128git38cd846-5
- Update to latest snapshot.

* Mon Nov 04 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6^20241101gitbe65dbb-4
- Update to latest snapshot.

* Tue Sep 24 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6^20240923git70ef8ee-3
- Use new packaging guidelines for snapshots.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6-2.20240423git73be2eb
- Update to latest snapshot.

* Sat Feb 17 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6-1
- Update to final 0.9.6.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 0.9.5-4.20240130gitbce97bd
- Update to latest snapshot.

* Wed Nov 15 2023 Simone Caronni <negativo17@gmail.com> - 0.9.5-3.20230617git5970c4c
- Drop custom signing and compressing in favour of kmodtool.

* Wed Jun 21 2023 Simone Caronni <negativo17@gmail.com> - 0.9.5-2.20230617git5970c4c
- Update to latest snapshot.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 0.9.5-1
- Update to 0.9.5.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 0.9.4-1
- Update to 0.9.4.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 0.9.3-1
- Update to release 0.9.3.

* Sun May 01 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-6.20220430git74ea7c1
- Update to latest snapshot, supports firmware 5.13.

* Sun Mar 20 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-5.20220306git4fd620c
- Update to latest snapshot, adds support for BLE firmware.

* Sun Jan 23 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-4.20211203gitcf392a7
- Update to latest snapshot.

* Tue Sep 14 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-3
- Add automatic signing workaround.

* Wed Aug 18 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-2
- Add module stripping.
- Fix module compression.

* Mon Aug 16 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-1
- First build.

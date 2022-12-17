%global commit0 74ea7c1488f9ccebf3ed6d9aea1319cacb08c625
%global date 20220430
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global mok_algo sha512
%global mok_key /usr/src/akmods/mok.key
%global mok_der /usr/src/akmods/mok.der

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_install_post}

%define __mod_install_post \
  if [ $kernel_version ]; then \
    find %{buildroot} -type f -name '*.ko' | xargs %{__strip} --strip-debug; \
    if [ -f /usr/src/akmods/mok.key ] && [ -f /usr/src/akmods/mok.der ]; then \
      find %{buildroot} -type f -name '*.ko' | xargs echo; \
      find %{buildroot} -type f -name '*.ko' | xargs -L1 /usr/lib/modules/${kernel_version%%___*}/build/scripts/sign-file %{mok_algo} %{mok_key} %{mok_der}; \
    fi \
    find %{buildroot} -type f -name '*.ko' | xargs xz; \
  fi

Name:           xpadneo-kmod
Version:        0.9.5
Release:        1%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Advanced Linux Driver for Xbox One Wireless Gamepad
License:        GPLv3
URL:            https://atar-axis.github.io/xpadneo

%if 0%{?tag:1}
Source0:        https://github.com/atar-axis/xpadneo/archive/v%{version}.tar.gz#/xpadneo-%{version}.tar.gz
%else
Source0:        https://github.com/atar-axis/xpadneo/archive/%{commit0}.tar.gz#/xpadneo-%{shortcommit0}.tar.gz
%endif


# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Advanced Linux Driver for Xbox One Wireless Gamepad.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
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

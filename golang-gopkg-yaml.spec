%{?scl:%scl_package %{name}}

%if 0%{?fedora} || 0%{?rhel} == 6|| 0%{?rhel} == 7
%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%define copying() \
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7 \
%license %{*} \
%else \
%doc %{*} \
%endif

%global provider        github
%global provider_tld    com
%global project         go-yaml
%global repo            yaml
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          d466437aa4adc35830964cffc5b5f262c63ddcb4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global import_path     gopkg.in/v2/yaml
%global import_path_sec gopkg.in/yaml.v2

%global v1_commit          1b9791953ba4027efaeb728c7355e542a203be5e
%global v1_shortcommit     %(c=%{v1_commit}; echo ${c:0:7})
%global v1_import_path     gopkg.in/v1/yaml
%global v1_import_path_sec gopkg.in/yaml.v1


Name:           %{?scl_prefix}golang-gopkg-yaml
Version:        1
Release:        9%{?dist}
Summary:        Enables Go programs to comfortably encode and decode YAML values
License:        LGPLv3 with exceptions
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/yaml-%{commit}.tar.gz
Source1:        https://%{provider_prefix}/archive/%{v1_commit}/yaml-%{v1_commit}.tar.gz

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:   %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%ifarch 0%{?gccgo_arches}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  %{?scl_prefix}golang(gopkg.in/check.v1)
%endif

Requires:       %{?scl_prefix}golang(gopkg.in/check.v1)

Provides:       %{?scl_prefix}golang(%{v1_import_path}) = %{version}-%{release}
Provides:       %{?scl_prefix}golang(%{v1_import_path_sec}) = %{version}-%{release}

%description devel
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package is almost compatible with YAML 1.1, including support for
anchors, tags, etc. There are still a few missing bits, such as document
merging, base-60 floats (huh?), and multi-document unmarshalling. These
features are not hard to add, and will be introduced as necessary.

This package contains library source intended for
building other packages which use import path with
%{v1_import_path} prefix.

%package devel-v2
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  %{?scl_prefix}golang(gopkg.in/check.v1)
%endif

Requires:       %{?scl_prefix}golang(gopkg.in/check.v1)

Provides:       %{?scl_prefix}golang(%{import_path}) = %{version}-%{release}
Provides:       %{?scl_prefix}golang(%{import_path_sec}) = %{version}-%{release}

%description devel-v2
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package supports most of YAML 1.1 and 1.2,
including support for anchors, tags, map merging, etc.
Multi-document unmarshalling is not yet implemented, and base-60 floats
from YAML 1.1 are purposefully not supported since they're a poor design
 and are gone in YAML 1.2.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:   %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%ifarch 0%{?gccgo_arches}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang
%endif

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}
Requires:        %{name}-devel-v2 = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n yaml-%{commit}
%setup -q -n yaml-%{v1_commit} -T -b 1

%build
%{?scl:scl enable %{scl} - << "EOF"}

%{?scl:EOF}
%install
%{?scl:scl enable %{scl} - << "EOF"}
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> v1_devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/$file
    echo "%%{gopath}/src/%%{v1_import_path_sec}/$file" >> v1_devel.file-list
done
pushd ../yaml-%{commit}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path_sec}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../yaml-%{v1_commit}/devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path_sec}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path_sec}/$file
    echo "%%{gopath}/src/%%{import_path_sec}/$file" >> ../yaml-%{v1_commit}/devel.file-list
done
popd
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> unit-test.file-list
done
pushd ../yaml-%{commit}
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../yaml-%{v1_commit}/unit-test.file-list
done
popd
%endif

%if 0%{?with_devel}
olddir=$(pwd)
pushd %{buildroot}/%{gopath}/src/%{import_path}
for file in $(find . -type d) ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$file" >> ${olddir}/devel.file-list
done
popd
echo "%%dir %%{gopath}/src/gopkg.in/v2" >> devel.file-list
echo "%%dir %%{gopath}/src/gopkg.in" >> devel.file-list

sort -u -o devel.file-list devel.file-list
%endif

%if 0%{?with_devel}
olddir=$(pwd)
pushd %{buildroot}/%{gopath}/src/%{import_path_sec}
for file in $(find . -type d) ; do
    echo "%%dir %%{gopath}/src/%%{import_path_sec}/$file" >> ${olddir}/devel.file-list
done
popd
echo "%%dir %%{gopath}/src/gopkg.in" >> devel.file-list

sort -u -o devel.file-list devel.file-list
%endif

%if 0%{?with_devel}
olddir=$(pwd)
pushd %{buildroot}/%{gopath}/src/%{v1_import_path}
for file in $(find . -type d) ; do
    echo "%%dir %%{gopath}/src/%%{v1_import_path}/$file" >> ${olddir}/v1_devel.file-list
done
popd
echo "%%dir %%{gopath}/src/gopkg.in/v1" >> v1_devel.file-list
echo "%%dir %%{gopath}/src/gopkg.in" >> v_1devel.file-list

sort -u -o v1_devel.file-list v1_devel.file-list
%endif

%if 0%{?with_devel}
olddir=$(pwd)
pushd %{buildroot}/%{gopath}/src/%{v1_import_path_sec}
for file in $(find . -type d) ; do
    echo "%%dir %%{gopath}/src/%%{v1_import_path_sec}/$file" >> ${olddir}/v1_devel.file-list
done
popd
echo "%%dir %%{gopath}/src/gopkg.in" >> v1_devel.file-list

sort -u -o v1_devel.file-list v1_devel.file-list
%endif

%{?scl:EOF}
%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%ifarch 0%{?gccgo_arches}
function gotest { %{gcc_go_test} "$@"; }
%else
%if 0%{?golang_test:1}
function gotest { %{golang_test} "$@"; }
%else
function gotest { go test "$@"; }
%endif
%endif

export GOPATH=%{buildroot}/%{gopath}:%{gopath}
gotest %{v1_import_path_sec}
pushd ../yaml-%{v1_commit}
gotest %{import_path_sec}
popd
%endif

%if 0%{?with_devel}
%files devel -f v1_devel.file-list
%copying LICENSE LICENSE.libyaml
%doc README.md

%files devel-v2 -f devel.file-list
%copying LICENSE LICENSE.libyaml
%doc README.md
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%copying LICENSE LICENSE.libyaml
%doc README.md
%endif

%changelog
* Wed Feb 3 2016 Marek Skalicky <mskalick@redhat.com> - 1-9
- Fixed directory ownership

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-8
- Choose the correct architecture
- Update unit-test subpackage
  related: #1250524

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-7
- Update spec file to spec-2.0
  resolves: #1250524

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 jchaloup <jchaloup@redhat.com> - 1-5
- Update to gopkg.in/check.v2 but still provide gopkg.in/check.v1
  related: #1141875

* Fri Oct 10 2014 jchaloup <jchaloup@redhat.com> - 1-4
- Adding go test and deps on gopkg.in/check.v1
- Adding another Provides

* Mon Sep 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-3
- Resolves: rhbz#1141875 - newpackage
- no debug_package
- preserve timestamps
- do not redefine gopath

* Thu Aug 07 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-2
- Fix import_path

* Tue Aug 05 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-1
- First package for Fedora

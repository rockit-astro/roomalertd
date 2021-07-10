Name:      observatory-roomalert-data
Version:   20210710
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert configuration files.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

%description

%build
mkdir -p %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/clasp.json %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/goto1.json %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/goto2.json %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/superwasp.json %{buildroot}%{_sysconfdir}/roomalertd/

%files
%defattr(-,root,root,-)
%{_sysconfdir}/roomalertd/clasp.json
%{_sysconfdir}/roomalertd/goto1.json
%{_sysconfdir}/roomalertd/goto2.json
%{_sysconfdir}/roomalertd/superwasp.json

%changelog

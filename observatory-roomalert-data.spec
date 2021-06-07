Name:      observatory-roomalert-data
Version:   20210607
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert configuration files.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-demjson, python3-warwick-observatory-common, python3-warwick-observatory-roomalert
Requires:  observatory-log-client, %{?systemd_requires}

%description

%build
mkdir -p %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/nites.json %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/goto.json %{buildroot}%{_sysconfdir}/roomalertd/
%{__install} %{_sourcedir}/superwasp.json %{buildroot}%{_sysconfdir}/roomalertd/

%files
%defattr(-,root,root,-)
%{_sysconfdir}/roomalertd/nites.json
%{_sysconfdir}/roomalertd/goto.json
%{_sysconfdir}/roomalertd/superwasp.json

%changelog

Name:      onemetre-roomalert-server
Version:   3.1.1
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-demjson, python3-warwick-observatory-common, python3-warwick-observatory-roomalert
Requires:  observatory-log-client, %{?systemd_requires}

%description
Part of the observatory software for the Warwick one-meter telescope.

roomalertd is a Pyro frontend for querying the Room Alert via http.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/roomalertd/

%{__install} %{_sourcedir}/roomalertd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/roomalertd.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/roomalertd/

%post
%systemd_post roomalertd.service

%preun
%systemd_preun roomalertd.service

%postun
%systemd_postun_with_restart roomalertd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalertd
%defattr(-,root,root,-)
%{_unitdir}/roomalertd.service
%{_sysconfdir}/roomalertd/onemetre.json

%changelog

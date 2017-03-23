Name:      goto-roomalert-server
Version:   1.10
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-demjson, python3-warwickobservatory, onemetre-obslog-client, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

%description
Part of the observatory software for the Warwick one-meter telescope.

roomalertd is a Pyro frontend for querying the Room Alert via http.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/roomalertd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/goto-roomalertd.service %{buildroot}%{_unitdir}

%pre
%service_add_pre goto-roomalertd.service

%post
%service_add_post goto-roomalertd.service

%preun
%stop_on_removal goto-roomalertd.service
%service_del_preun goto-roomalertd.service

%postun
%restart_on_update goto-roomalertd.service
%service_del_postun goto-roomalertd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalertd
%defattr(-,root,root,-)
%{_unitdir}/goto-roomalertd.service

%changelog

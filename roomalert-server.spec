Name:      onemetre-roomalert-server
Version:   1.0
Release:   1
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

%description
Part of the observatory software for the Warwick one-meter telescope.

roomalertd is a Pyro frontend for querying the Room Alert via http.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/roomalertd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/roomalertd.service %{buildroot}%{_unitdir}

%pre
%service_add_pre roomalertd.service

%post
%service_add_post roomalertd.service
%fillup_and_insserv -f -y roomalertd.service

# Install python dependencies
# This is horrible, but it seems to be the only way that actually works!
pip3 install demjson Pyro4

%preun
%stop_on_removal roomalertd.service
%service_del_preun roomalertd.service

%postun
%restart_on_update roomalertd.service
%service_del_postun roomalertd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalertd
%defattr(-,root,root,-)
%{_unitdir}/roomalertd.service

%changelog

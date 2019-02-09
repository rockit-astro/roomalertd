Name:      goto-roomalert-server
Version:   2.2.0
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python36, python36-Pyro4, python36-demjson, python36-warwick-observatory-common
Requires:  observatory-log-client, %{?systemd_requires}

%description
Part of the observatory software for the Warwick La Palma telescopes.

roomalertd is a Pyro frontend for querying the Room Alert via http.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/roomalertd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/goto-roomalertd.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/superwasp-roomalertd.service %{buildroot}%{_unitdir}

%post
%systemd_post goto-roomalertd.service
%systemd_post superwasp-roomalertd.service

%preun
%systemd_preun goto-roomalertd.service
%systemd_preun superwasp-roomalertd.service

%postun
%systemd_postun_with_restart goto-roomalertd.service
%systemd_postun_with_restart superwasp-roomalertd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalertd
%defattr(-,root,root,-)
%{_unitdir}/goto-roomalertd.service
%{_unitdir}/superwasp-roomalertd.service

%changelog

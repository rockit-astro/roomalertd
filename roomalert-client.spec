Name:      onemetre-roomalert-client
Version:   1.3
Release:   1
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert client for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3

%description
Part of the observatory software for the Warwick one-meter telescope.

roomalert is a commandline utility that queries the Room Alert daemon.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/roomalert %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/roomalert %{buildroot}/etc/bash_completion.d/roomalert

# Install python dependencies
# This is horrible, but it seems to be the only way that actually works!
pip3 install Pyro4

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalert
/etc/bash_completion.d/roomalert

%changelog

Name:      observatory-roomalert-client
Version:   20211127
Release:   0
Url:       https://github.com/warwick-one-metre/roomalertd
Summary:   Room Alert client.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwick-observatory-common, python3-warwick-observatory-roomalert

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/roomalert %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/roomalert %{buildroot}/etc/bash_completion.d/roomalert

%files
%defattr(0755,root,root,-)
%{_bindir}/roomalert
/etc/bash_completion.d/roomalert

%changelog

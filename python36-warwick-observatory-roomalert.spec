Name:           python36-warwick-observatory-roomalert
Version:        3.0.0
Release:        0
License:        GPL3
Summary:        Common backend code for the RoomAlert daemons.
Url:            https://github.com/warwick-one-metre/roomalertd
BuildArch:      noarch

%description
Part of the observatory software for the Warwick La Palma telescopes.

python36-warwick-observatory-roomalert holds the common roomalert code.

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog

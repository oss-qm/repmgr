%global pkg_main		postgresql%postgres_major-repmgr

%global pg_prefix		/usr/lib/postgresql%postgres_major/
%global pg_bindir		%pg_prefix/bin
%global pg_config		%pg_bindir/pg_config

%global cmd_update_alt		%{_sbindir}/update-alternatives
%global pg_alternative_prio	%{postgres_major}00

Summary:	Replication manager for PostgreSQL
Name:		repmgr
Version:	5.1.0
Release:	mtx.9%{?dist}
License:	ISC
Group:		Database
Source:		repmgr-%version.tar.gz

BuildRoot:	%_tmppath/%name-root

BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	flex
BuildRequires:	postgresql%postgres_major-devel

## FIXME: for some strange reason, these deps dont come from postgresql
BuildRequires:	zlib-devel
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
BuildRequires:	libxslt-devel
BuildRequires:	readline-devel
BuildRequires:	libselinux-devel

%description
Replication manager for PostgreSQL %postgres_major

%package -n %pkg_main
Summary:		Replication manager for PostgreSQL %postgres_major
Requires:		postgresql%postgres_major
Requires(post):		%cmd_update_alt
Requires(postun):	%cmd_update_alt

%description -n %pkg_main
Replication manager for PostgreSQL %postgres_major

%post -n %pkg_main
# Create alternatives entries for common binaries and man files
%cmd_update_alt --install %{_bindir}/repmgr pgsql-repmgr %pg_bindir/repmgr %pg_alternative_prio

%preun -n %pkg_main
# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]; then
    %cmd_update_alt --remove pgsql-repmgr  %pg_bindir/repmgr
fi

%prep

%if 0%{?postgres_major:1}
echo "Building against PostgreSQL %postgres_major"
%else
echo "postgres_major needs to be defined" >&2
exit 1
%endif

%setup -q -n repmgr-%version

%build
autoreconf -fi
PG_CONFIG=%pg_config %configure \
    --bindir=`%pg_config --bindir` \
    --sysconfdir=%_sysconfdir \
    --libdir=`%pg_config --libdir` \
    --docdir=`%pg_config --docdir`
make %{?_smp_mflags}

%check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

( cd %buildroot ; \
    find * -type f -exec "echo" "/{}" ";" ; \
    find * -type l -exec "echo" "/{}" ";" ; \
) > %pkg_main.files

%files -n %pkg_main -f %pkg_main.files
%defattr(-,root,root)
%doc *.md HISTORY COPYRIGHT CREDITS LICENSE
%dir /

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 11 2020 Enrico Weigelt, metux IT consult <info@metux.net> - 5.1.0-mtx.3
- packaged for SLES12

* Thu Jul 12 2018 Patsy Franklin <pfrankli@redhat.com> - 3.0.4-2
- Build requires gcc-c++ for building from source. (#1600084)

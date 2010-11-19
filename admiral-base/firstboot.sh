# This script will run the first time the virtual machine boots
# It is run as root.

echo "*****FIRST BOOT*****"

smbpasswd -s -a admiral <<END
%{PASSWORD}
%{PASSWORD}
END

a2enmod authnz_ldap
a2enmod ssl
a2ensite default-ssl

#a2enmod webauth
#a2enmod auth_kerb
#ln -s /var/lib/webauth /etc/apache2/webauth
#cp /root/webauth.keytab /etc/apache2/webauth/keytab
#chgrp www-data /etc/apache2/webauth/keytab
#chmod u=rw,g=r,o= /etc/apache2/webauth/keytab
#cp /root/krb5.keytab /etc/krb5.keytab
#chmod u=rw,go= /etc/krb5.keytab
#cp /root/webdav.keytab /etc/apache2/webdav.keytab
#chown root:www-data /etc/apache2/webdav.keytab
#chmod 640 /etc/apache2/webdav.keytab

mkdir /home/data
chown www-data: /home/data
chmod g+ws /home/data
cp /root/ADMIRAL.README /home/data

chmod +x /root/make-apache2-cert.sh
/root/make-apache2-cert.sh %{HOSTNAME}.zoo.ox.ac.uk
cp /root/apache-default-ssl /etc/apache2/sites-available/default-ssl

a2enmod dav
a2enmod dav_fs
mkdir /usr/share/apache2/var
touch /usr/share/apache2/var/DAVlock
chown -R www-data:www-data /usr/share/apache2/var
mv /etc/apache2/sites-available/default /etc/apache2/sites-available/default_orig
cp /root/apache-default /etc/apache2/sites-available/default

a2enmod proxy
a2enmod proxy_http
cp /root/apache-databank-proxy /etc/apache2/sites-available/databank-proxy
ln -s /etc/apache2/sites-available/databank-proxy /etc/apache2/sites-enabled/databank-proxy

/etc/init.d/apache2 restart

gunzip /usr/share/doc/smbldap-tools/configure.pl.gz
adduser openldap ssl-cert

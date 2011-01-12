#!/bin/bash

if [[ "$1" == "" ]]; then
    echo "Usage:"
    echo "  $0 username"
    echo "      Generate system configuration for named user" 
    echo ""
    echo "  $0 all password"
    echo "      Generate system configuration for all recorded ADMIRAL users" 
    echo "      Each user gets a password of the form 'username-password',"
    echo "      which they should change on first login." 
    echo ""
    exit
fi

if [[ "$1" == "all"]]; then
    if [[ "$2" == "" ]]; then
        echo "Provide password suffix when regenerating all user accounts"
    fi
else
    if [[ ! -e /root/admiralconfig.d/admiralresearchgroupmembers/$1.sh ]]; then
        echo "No such user recorded: $1"
        exit
    fi
fi
 
source /root/admiralconfig.d/admiralconfig.sh

function generatesystemuser()
{
    # $1 = users script name 
    # $2 = new user password
    source $1
    password=$username-$2
    echo $username $userfullname $userrole $userroom $userphone $password

    if [[ "$userrole" != "RGCollaborator" ]]; then
    
      # Create new user account
    
      if [[ "$password" == "" ]]; then
        smbldap-useradd -a -P -m -g $userrole $username
      else
        smbldap-useradd -a -P -m -g $userrole $username <<END
$password
$password
END
      fi
      smbldap-userinfo -f "$userfullname" -r "$userroom" -w "$userphone" $username
    
      mv /home/$1 /home/$1-saved
      ln -s /mnt/lv-admiral-data/home/$username /home/$username
    
      # Set default file system access modes (overridden by access control lists)
    
      chown --recursive $username:$userrole /home/data/private/$username
      chown --recursive $username:$userrole /home/data/shared/$username
      chown --recursive $username:$userrole /home/data/collab/$username
    
      # Set access control lists on new user directories
    
      # remove previous ACLs
      setfacl --recursive --remove-all /home/data/private/$username
      setfacl --recursive --remove-all /home/data/shared/$username
      setfacl --recursive --remove-all /home/data/collab/$username
    
      # User access
      setfacl --recursive -m u:$username:rwx /home/data/private/$username
      setfacl --recursive -m u:$username:rwx /home/data/shared/$username
      setfacl --recursive -m u:$username:rwx /home/data/collab/$username
    
      # Research group leader access
      setfacl --recursive -m g:RGLeader:rx /home/data/private/$username
      setfacl --recursive -m g:RGLeader:rx /home/data/shared/$username
      setfacl --recursive -m g:RGLeader:rx /home/data/collab/$username
    
      # Research group member access
      setfacl --recursive -m g:RGMember:rx /home/data/shared/$username
      setfacl --recursive -m g:RGMember:rx /home/data/collab/$username
    
      # Research group collaborator access
      setfacl --recursive -m g:RGCollaborator:rx /home/data/collab/$username
    
      # Web server access
      setfacl --recursive -m u:www-data:rwx /home/data/private/$username
      setfacl --recursive -m u:www-data:rwx /home/data/shared/$username
      setfacl --recursive -m u:www-data:rwx /home/data/collab/$username
    
      # Copy access modes to default access modes
      getfacl --access /home/data/private/$username | setfacl -d -M- /home/data/private/$username
      getfacl --access /home/data/shared/$username  | setfacl -d -M- /home/data/shared/$username
      getfacl --access /home/data/collab/$username  | setfacl -d -M- /home/data/collab/$username
    
      # Set up Apache access control configuration
      /root/createapacheuserconfig.sh $username
    
    fi
    
    if [[ "$userrole" == "RGCollaborator" ]]; then
    
      if [[ "$password" == "" ]]; then
        smbldap-useradd -a -P -m -s /bin/false -g $userrole $username
      else
        smbldap-useradd -a -P -m -s /bin/false -g $userrole $username <<END
$password
$password
END
      fi
    
      smbldap-userinfo -f "$userfullname" -r "$userroom" -w "$userphone" $username
    
    fi
}

# Process all user files in /root/admiralconfig.d/a/root/admiralresearchgroupmembers

if [[ "$1" == "all" ]]; then
    for u in `ls /root/admiralconfig.d/admiralresearchgroupmembers/*.sh`; do
        generatesystemuser $u $2
    done
elif [[ -e "/root/admiralconfig.d/admiralresearchgroupmembers/$1.sh" ]]; then
    generatesystemuser /root/admiralconfig.d/admiralresearchgroupmembers/$1.sh    
else
    echo "No such user ($1)"
fi

# End.

#!/bin/bash

if [[ $(id -u) -ne 0 ]];
then
    printf "Please run the script as root"
    exit 1;
fi


printf "[*] Fetching all users from the AD\n"
/home/pentest/Documents/scripts/bruteforce/ldap_users.py


# The first argument is the file created by hashcat_to_uncracked.py
printf "[*] Searching for users with passwords found\n"
/home/pentest/Documents/scripts/bruteforce/ldap_users_pass.py /home/pentest/Documents/scripts/bruteforce/resultats/all_users.txt "$1"

printf "[*] Searching for admins with found password\n"
/home/pentest/Documents/scripts/bruteforce/ldap_users_pass.py /home/pentest/Documents/scripts/bruteforce/resultats/user_admin.txt "$1" -o resultats/admins_pass.txt

printf "[*] Searching for service accounts with found password\n"
/home/pentest/Documents/scripts/bruteforce/ldap_users_pass.py /home/pentest/Documents/scripts/bruteforce/resultats/serv_accts.txt "$1" -o resultats/serv_accts_pass.txt

printf "[*] Deleting files\n"
rm -f resultats/all_users.txt
rm -f resultats/user_admin.txt
rm -f resultats/serv_accts.txt

printf "[*] Attributing restrictive rights to the new files (chmod 600)\n"
chmod 600 resultats/users_pass.txt
chmod 600 resultats/admins_pass.txt
chmod 600 resultats/serv_accts_pass.txt

printf "[*] Number of users with cracked passwords found: "
wc -l /home/pentest/Documents/scripts/bruteforce/resultats/users_pass.txt

printf "[*] Number of admins with cracked passwords found: "
wc -l /home/pentest/Documents/scripts/bruteforce/resultats/admins_pass.txt


printf "[*] Number of service accounts with cracked passwords found: "
wc -l /home/pentest/Documents/scripts/bruteforce/resultats/serv_accts_pass.txt

printf "[*] END\n"

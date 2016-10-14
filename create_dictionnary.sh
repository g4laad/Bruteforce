#!/bin/bash

if [[ $(id -u) -ne 0 ]];
then 
    printf "Please run the script as root";
    exit 1;
fi

printf "[*] Creating dictionnary from john.pot and hashcat.pot\n"
printf "Temp file: /tmp/unsorted.dico.txt\n"
printf "New dictionnary: /home/pentest/dico.txt\n"

unsorted_dico=/tmp/unsorted_dico.txt
new_dico=/home/pentest/Documents/dictionnaire/dico.txt


cat $new_dico >> $unsorted_dico
cat /opt/john/run/john.pot | cut -d":" -f2 >> $unsorted_dico
cat /opt/hashcat/hashcat.pot | cut -d":" -f2 >> $unsorted_dico

printf "[*] Deleting /home/pentest/dico.txt\n"
rm -f $new_dico

printf "[*] Creating the new dico.txt\n"
cat $unsorted_dico | sort | uniq  > $new_dico

printf "[*] Deleting temp file\n"
rm -f $unsorted_dico
 
printf "END\n"

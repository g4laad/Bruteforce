#!/bin/bash

printf "[*] John The Ripper\n" 
printf "[*] Single mode\n"
/opt/john/run/john --single --format=NT --encoding=cp850 --fork=8 "$1"
printf "[*] Dictionnary mode\n"
/opt/john/run/john --wordlist="$2" --format=NT --encoding=cp850 --fork=8 "$1"
printf "[*] Incremental mode\n"
/opt/john/run/john --incremental --format=nt-opencl  --encoding=cp850 --fork=8 "$1"
print "[*] END"

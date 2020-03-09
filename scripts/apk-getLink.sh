#/bin/bash
packagename=$1
rootLinkFinder=$2
`apktool d $packagename.apk`;
cd $packagename;
mkdir collection;
grep -rihEo   "http[s]*://([a-zA-Z0-9]+\.){1,26}[a-zA-Z0-9]+" . | grep -v "schemas.android" | grep -v "Binary file" | sort | uniq >> ./../findlink.txt
find . -name \*.smali -exec sh -c "cp {} collection/\$(head /dev/urandom | md5 | cut -d ' ' -f1).smali" \; ;
python3 $2/linkfinder.py -i 'collection/*.smali' -o cli |grep -Eo  "http[s]*://([a-zA-Z0-9]+\.){1,26}[a-zA-Z0-9]+"|sort |uniq >> ./../findlink.txt;

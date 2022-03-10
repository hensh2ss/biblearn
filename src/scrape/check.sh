#!/bin/bash

# this script checks every bible version folder it finds in ./
# it counts all xml files for a given book and makes sure there is one per chapter for that book

mistakes=0

for line in $(cat bible_meta.txt)
do
	book=$(echo $line | cut -d : -f 1)
	chaps=$(echo $line | cut -d : -f 2)
	for v in $(find . -mindepth 1 -type d | grep -v idea)
	do
		chaps2=$(ls -ltr $v | grep -c "${book}[0-9]*.xml")
		if [[ $chaps2 -ne $chaps ]]
		then
			((mistakes++))
			echo "only $chaps2 chapters for $v/$book, expected $chaps"
		fi
	done
done

if [[ $mistakes -eq 0 ]]
then
	echo "All checks out"
fi

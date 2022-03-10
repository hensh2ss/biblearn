#!/bin/bash

# this script uses curl to get all books/chapters of a given version from blue letter bible
# html comes back, and the relevant portions are grepped and saved to an xml file
# one xml per chapter, expect 1189 total

version=$1
book=$2
mkdir -p $version

function do_book() {
  local line=$1
  local book=$(echo $line | cut -d : -f 1)
	chaps=$(echo $line | cut -d : -f 2)

	# for each chapter in the book
	for ((c=1; c<=$chaps; c++))
	do
		while true
		do
			divs=$(curl https://www.blueletterbible.org/$version/$book/$c/ | grep 'div class="scriptureText"' | sed 's/&nbsp//g' | sed 's/<[/]*p[/a-z=" ]*>//g' | sed 's/<[/]*em[/a-z=" ]*>//g')
			echo "<root> $divs </root>" > ${version}/${book}${c}.xml
			verses=$(wc -l ${version}/${book}${c}.xml | sed 's/[ ]*\([0-9]*\) .*/\1/g')
			if [[ $verses -le 1 ]]
			then
				sleep 60
			else
				break
			fi
		done
	done
	echo ${version}/${book}
}

if [[ -z $book || $book == "" ]]
then
  # for each book of the bible
  for line in $(cat bible_meta.txt)
  do
    do_book $line
  done
else
  line=$(grep $book bible_meta.txt)
  do_book $line
fi

#!/bin/bash

# scrape.sh produced xml files, one per chapter
# this script gathers all chapter xmls for a book and
# uses xpath to pull out the raw verse text
# outputs one json per book

version=$1
book=$2
mkdir -p $version

function do_book() {
  local line=$1
  local book=$(echo $line | cut -d : -f 1)
	echo "{" > ${version}/${book}.json
	chaps=$(echo $line | cut -d : -f 2)

	# for each chapter in the book
	for ((c=1; c<=$chaps; c++))
	do
		echo "\"$c\": [" >> ${version}/${book}.json

		# for each verse in the chapter
		verses=$(wc -l ${version}/${book}${c}.xml | sed 's/[ ]*\([0-9]*\) .*/\1/g')
		for ((v=1; v<=$verses; v++))
		do
		  # get the text out of the xml
			text=$(xpath -q -e '/root/div['$v']/div/text()' ${version}/${book}${c}.xml | tr -d '\012\015' | tr \" \')
			if [[ -z $text ]]
			then
			  # if the text is empty search in the div/span
				text=$(xpath -q -e '/root/div['$v']/div/span/text()' ${version}/${book}${c}.xml | tr -d '\012\015' | tr \" \')
			fi
			if [[ $v -eq $verses ]]
			then
				echo "{\"verse\": $v, \"text\": \"$text\"}" >> ${version}/${book}.json
			else
				echo "{\"verse\": $v, \"text\": \"$text\"}," >> ${version}/${book}.json
			fi
		done
		if [[ $c -eq $chaps ]]
		then
			echo "]" >> ${version}/${book}.json
		else
			echo "]," >> ${version}/${book}.json
		fi
	done
	echo "}" >> ${version}/${book}.json
	echo $version/$book
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

python3 missing_verses.py $version

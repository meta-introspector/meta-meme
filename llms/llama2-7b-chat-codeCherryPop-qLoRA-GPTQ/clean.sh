for x in clarifai_*.txt;
do
    echo $x
    grep -v __input_line $x |gron -u |jq ".[]|.[]" -r | sort -u > $x.out;
done

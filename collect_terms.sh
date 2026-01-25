pushd meta-meme/
git log --all --patch > patch.txt
popd
pushd cd meta-meme.wiki
git log --patch --all > patch.txt
popd
cp ./meta-meme.wiki/patch.txt meta-meme/wiki-patch.txt
pushd meta-meme/
cat wiki-patch.txt patch.txt >total.txt
grep -P  -o -e '([a-zA-Z0-9]+)' total.txt  |sort |uniq -c | sort -n >tokens.txt
popd

  548  cd 2023/08/20/
  549  git clone https://github.com/meta-introspector/meta-meme
  550  cd meta-meme/
  551  ls


# what i want to wrute to export the data
  553  gh_export_discussion --org "meta-introspector" --repo "meta-meme" --depth=21 ---first=10 --apply=emojify 

  
#  what i want to write 
  554  gh_export discussion/meta-introspector/meta-meme/filter=thread==21/filter=first=10/map-apply=emojify 
  555  bash gh_export_discussion.sh 
  558  mkdir -p data/meta-introspector/metameme/dicussions/21/head.json
  557  #bash gh_export_discussion.sh  > data/meta-introspector/metameme/dicussions/21/head.json
  559  history 
  560  history  > readme.md

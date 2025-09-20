source "$(dirname "$0")"/../../../../scripts/lib_git_submodule.sh

#the commit loop

while [ 1 ]
do
      git_add_all
      git_commit_message "step"
#      git push origin
      push_to_origin_branch "docs"
      sleep 10
done

source "$(dirname "$0")"/../../../../scripts/lib_git_submodule.sh

find -name \*.md | xargs grep .  > total.txt
git_commit_message "update total"
push_to_origin_branch "HEAD"

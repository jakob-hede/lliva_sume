fail() {
  echo "Error: $*" >&2
  exit 1
}

splitxecute() {
  echo 'splitxecute'
  declare media_dir='/opt/projects/liva_sume/media/1'
  cd $media_dir || fail "cd $media_dir"
  ls -l
  input_file='split.sh'

}

splitxecute

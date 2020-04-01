my_dir="$(dirname "$0")"
source "$my_dir/variables.sh"


if [ ! $(gsutil ls -b $DATA_BUCKET) ]
then
  gsutil mb -p $PROJECT_ID $DATA_BUCKET
fi

my_dir="$(dirname "$0")"
source "$my_dir/variables.sh"


for q in 'hinduism' 'bible' 'buddhism' 'islam' 'judaism'
do
  python3 -m dsba6155project.data_pull.gutenberg --query $q --folder-clean False
done


gsutil -m cp -r "$my_dir/../dsba6155project/data" "$DATA_BUCKET/books/"

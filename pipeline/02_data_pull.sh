for q in 'hinduism' 'bible' 'buddhism' 'islam' 'judaism'
do
  python3 -m dsba6155project.data_pull.gutenberg --query $q --folder-clean False
done

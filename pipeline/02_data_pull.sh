git clone https://github.com/abhijeetdtu/dsba6155project

cd dsba6155project

python3 -m pip install -r requirements.txt --user

for q in 'hinduism' 'bible' 'buddhism' 'islam' 'judaism'
do
  python3 -m dsba6155project.data_pull.gutenberg --query $q --folder-clean False
done

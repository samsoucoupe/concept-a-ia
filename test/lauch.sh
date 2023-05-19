variable="Cruche"
python3 utils/dot_solution.py $variable true
mkdir -p PNG/$variable

rm -rf PNG/$variable/*

list=$(ls DOT/$variable)

for i in $list
do
  dot -Tpng DOT/$variable/$i -o PNG/$variable/$i.png
done
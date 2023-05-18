variable="Cruche"
river="false"

mkdir -p PNG/$variable
mkdir -p DOT/$variable


rm -rf PNG/$variable/*
rm -rf DOT/$variable/*

python3 utils/converter.py -r $river -type xtd --input XML/$variable.xml --output DOT/$variable/$variable.dot
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 12 -print 0 -resultsType 1 -crossingRiver $river -file  XML/$variable.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 12 -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml > TXT/$variable.txt
python3 test/dot_solution.py $variable

list=$(ls DOT/$variable)

for i in $list
do
  dot -Tpng DOT/$variable/$i -o PNG/$variable/$i.png
done
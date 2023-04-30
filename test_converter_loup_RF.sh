#River False :
variable="LoupChevreSaladeEtudiant"
python3 utils/converter.py -r False -type xtd -input XML/$variable.xml -output DOT/test/$variable.dot
dot -Tpng DOT/test/$variable.dot -o PNG/test/$variable.png
python3 utils/converter.py -r False -type dtx -input DOT/test/$variable.dot -output XML/test/$variable.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file  XML/test/$variable.xml

# Path: test_converter_loup_RF.sh
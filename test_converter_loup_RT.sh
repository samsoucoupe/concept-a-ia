#River True :
variable="LoupChevreSaladeEtudiant"
python3 utils/converter.py -r True -type xtd -input XML/$variable.xml -output DOT/test/$variable.dot
dot -Tpng DOT/test/$variable.dot -o PNG/test/$variable.png
python3 utils/converter.py -r True -type dtx -input DOT/test/$variable.dot -output XML/test/$variable.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver True -file  XML/test/$variable.xml


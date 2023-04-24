#River False:
python3 utils/converter.py -r False -type xtd -input XML/sceau.xml -output DOT/test/sceau.dot ; dot -Tpng DOT/test/sceau.dot -o PNG/test/sceau.png
python3 utils/converter.py -r False -type dtx -input DOT/test/sceau.dot -output XML/test/sceau.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file  XML/test/sceau.xml


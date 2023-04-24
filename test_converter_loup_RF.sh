#River False :
python3 utils/converter.py -r False -type xtd -input XML/LoupChevreSalade.xml -output DOT/test/LoupChevreSalade.dot ; dot -Tpng DOT/test/LoupChevreSalade.dot -o PNG/test/LoupChevreSalade.png
python3 utils/converter.py -r False -type dtx -input DOT/test/LoupChevreSalade.dot -output XML/test/LoupChevreSalade.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file  XML/test/LoupChevreSalade.xml

# Path: test_converter_loup_RF.sh
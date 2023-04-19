
python3 générateur_de_test.py ; python3 generator_file_general.py -name sceau -t ;python3 converter.py -r False -type xtd -input test.xml -output test.dot;dot -Tpng test.dot -o test.png;java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file test.xml


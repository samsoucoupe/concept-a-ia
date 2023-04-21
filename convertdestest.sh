#python3 générateur_de_test.py ; python3 generator_file_general.py -name sceau -t ;python3 converter.py -r False -type xtd -input test.xml -output test.dot;dot -Tpng test.dot -o test.png;java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file test.xml
#python3 test/convertertest.py -r False -type xtd -input sceau.xml -output test/sceautest.dot ; dot -Tpng test/sceautest.dot -o test/sceautest.png;
#python3 test/convertertest.py -r False -type dtx -input test/sceautest.dot -output test/sceautest.xml;
python3 test/convertertest.py -r True -type xtd -input LoupChevreSalade.xml -output test/sceautest.dot ; dot -Tpng test/sceautest.dot -o test/sceautest.png;

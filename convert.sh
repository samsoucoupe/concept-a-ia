#python3 converter.py -r True -type xtd -input LoupChevreSalade.xml -output LoupChevreSalade.dot ; dot -Tpng LoupChevreSalade.dot -o LoupChevreSalade.png
#python3 converter.py -r False -type xtd -input LoupChevreSalade.xml -output LoupChevreSalade.dot ; dot -Tpng LoupChevreSalade.dot -o LoupChevreSalade.png
#python3 converter.py -r False -type xtd -input sceau.xml -output sceau.dot ; dot -Tpng sceau.dot -o sceau.png
python3 générateur.py ; python3 generator_file_general.py -name sceau ;python3 converter.py -r False -type xtd -input sceau.xml -output sceau.dot;dot -Tpng sceau.dot -o sceau.png;java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file sceau.xml
#python3 converter.py -r False -type xtd -input sceau.xml -output sceau.dot ; dot -Tpng sceau.dot -o sceau.png;java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file sceau.xml

#on va test si test/convertdestest.py marche bien en prenant des fichiers xml les transformant en dot et en png

python3 converter.py -r True -type xtd -input LoupChevreSalade.xml -output LoupChevreSalade.dot ; dot -Tpng LoupChevreSalade.dot -o LoupChevreSalade.png
python3 test/convertertest.py -r True -type xtd -input LoupChevreSalade.xml -output test/LoupChevreSalade.dot ; dot -Tpng test/LoupChevreSalade.dot -o test/LoupChevreSalade.png
python3 test/convertertest.py -r True -type dtx -input test/LoupChevreSalade.dot -output test/LoupChevreSalade.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver True -file test/LoupChevreSalade.xml

#
#python3 test/convertertest.py -r False -type xtd -input LoupChevreSalade.xml -output test/LoupChevreSalade.dot ; dot -Tpng test/LoupChevreSalade.dot -o test/LoupChevreSalade.png
#python3 test/convertertest.py -r False -type dtx -input test/LoupChevreSalade.dot -output test/LoupChevreSalade.xml
#java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file test/LoupChevreSalade.xml


#idem pour le fichier sceau.xml

python3 test/convertertest.py -r True -type xtd -input sceau.xml -output test/sceau.dot ; dot -Tpng test/sceau.dot -o test/sceau.png
python3 test/convertertest.py -r True -type dtx -input test/sceau.dot -output test/sceau.xml
#java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver True -file test/sceau.xml

#python3 test/convertertest.py -r False -type xtd -input sceau.xml -output test/sceau.dot ; dot -Tpng test/sceau.dot -o test/sceau.png
#python3 test/convertertest.py -r False -type dtx -input test/sceau.dot -output test/sceau.xml
#java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file test/sceau.xml

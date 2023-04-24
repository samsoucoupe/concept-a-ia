#Xml to Dot :
#   River True : 
#   python3 test/convertertest.py -r True -type xtd -input sceau.xml -output test/sceau.dot ; dot -Tpng test/sceau.dot -o test/sceau.png

#   River False :
#   python3 test/convertertest.py -r False -type xtd -input sceau.xml -output test/sceau.dot ; dot -Tpng test/sceau.dot -o test/sceau.png


#Dot to Xml :
#   River True :
#   python3 test/convertertest.py -r True -type dtx -input test/sceau.dot -output test/sceau.xml
#   java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver True -file test/sceau.xml

#   River False :
#   python3 test/convertertest.py -r False -type dtx -input test/sceau.dot -output test/sceau.xml
#   java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file test/sceau.xml
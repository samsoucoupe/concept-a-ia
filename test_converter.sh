#River False:
variable="zodice"
# nom du fichier
echo "Enter the name of the file (without the extension):"
#read variable
# nom du fichier
# shellcheck disable=SC1007



python3 utils/converter.py -r True -type xtd -input XML/$variable.xml -output DOT/test/$variable.dot
dot -Tpng DOT/test/$variable.dot -o PNG/test/$variable.png
python3 utils/converter.py -r True -type dtx -input DOT/test/$variable.dot -output XML/test/$variable.xml
#java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver True -file  XML/$variable.xml
echo ""
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver False -file  XML/test/$variable.xml

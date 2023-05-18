utils/Interface/Introduction.sh


echo "Do you want to use the rules in the Rules folder (True or False):"
read use
if [ $use = "True" ] || [ $use = "true" ]
then
  echo "List of the rules in the Rules folder:"
  ls Rules/
  echo "Enter the name of the file ( For example: Rules_LCS.json => LCS):"
  read variable
else
  echo "Enter a name for the rules:"
  read variable
  python3 utils/question.py --nom_fichier $variable
fi

echo "The problem is: $variable"
echo "Is it a river problem ? (True or False):"
read river
if [ $river = "True" ] || [ $river = "true" ]
then
  echo "The problem is a river crossing problem"
  river="true"
else
  echo "The problem is not a river crossing problem"
  river="false"
fi


python3 utils/generator.py --rulesfiles Rules/Rules_$variable.json --output XML/test/$variable.xml
python3 utils/converter.py -r $river -type xtd -input XML/test/$variable.xml -output DOT/test/$variable.dot
dot -Tpng DOT/test/$variable.dot -o PNG/test/$variable.png
java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver $river -file  XML/test/$variable.xml

utils/Interface/Conclution.sh
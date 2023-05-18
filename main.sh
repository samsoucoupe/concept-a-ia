################################################################################
# Copyright (c) 2023. Samy Ben dhiab All rights reserved.                      #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License");           #
#    you may not use this file except in compliance with the License.          #
#    You may obtain a copy of the License at                                   #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#     Unless required by applicable law or agreed to in writing, software      #
#     distributed under the License is distributed on an "AS IS" BASIS,        #
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
#     See the License for the specific language governing permissions and      #
#     limitations under the License.                                           #
################################################################################

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
  python3 utils/question.py nom_fichier $variable
  python3 utils/generator.py --rulesfiles Rules/Rules_$variable.json --output XML/$variable.xml

fi

echo "The problem is: $variable"

#nombre de coup max pour la solution
echo "Enter the maximum number of moves for the solution:"
read max

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



mkdir -p PNG/$variable
mkdir -p DOT/$variable


rm -rf PNG/$variable/*
rm -rf DOT/$variable/*



if [ $river = "True" ] || [ $river = "true" ]
then
  python3 utils/converter.py -r true -type xtd --input XML/$variable.xml --output DOT/$variable/$variable.dot
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver true -file  XML/$variable.xml
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml > TXT/$variable.txt
  python3 utils/dot_solution.py $variable true
else
  python3 utils/converter.py -r false -type xtd --input XML/$variable.xml --output DOT/$variable/$variable.dot
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml > TXT/$variable.txt
  python3 utils/dot_solution.py $variable false
fi


list=$(ls DOT/$variable)

for i in $list
do
  dot -Tpng DOT/$variable/$i -o PNG/$variable/$i.png
done


utils/Interface/Conclution.sh
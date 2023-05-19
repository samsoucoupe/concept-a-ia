################################################################################
# Copyright (c) 2023. Samy Ben Dhiab (Samsoucoupe) All rights reserved.        #
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


variable=$2
max=$3
river=$1


if [ $river = "true" ]
then
  mkdir -p PNG/$variable"_River"
  mkdir -p DOT/$variable"_River"
  rm -rf PNG/$variable"_River"/*
  rm -rf DOT/$variable"_River"/*
  python3 utils/converter.py -r true -type xtd --input XML/$variable.xml --output DOT/$variable"_River"/$variable.dot
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver true -file  XML/$variable.xml
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml > TXT/$variable"_River".txt
  python3 utils/dot_solution.py $variable true
  list=$(ls DOT/$variable"_River")
  for i in $list
    do
      file_name=$(echo $i | cut -d'.' -f1)
      dot -Tpng DOT/$variable"_River"/$i -o PNG/$variable"_River"/$file_name.png
    done

else
  mkdir -p PNG/$variable
  mkdir -p DOT/$variable
  rm -rf PNG/$variable/*
  rm -rf DOT/$variable/*
  python3 utils/converter.py -r false -type xtd --input XML/$variable.xml --output DOT/$variable/$variable.dot
  java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n $max -print 0 -resultsType 1 -crossingRiver false -file  XML/$variable.xml > TXT/$variable.txt
  python3 utils/dot_solution.py $variable false
  list=$(ls DOT/$variable)
  for i in $list
    do
      file_name=$(echo $i | cut -d'.' -f1)
      dot -Tpng DOT/$variable/$i -o PNG/$variable/$file_name.png
    done
fi
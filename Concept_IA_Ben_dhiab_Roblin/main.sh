################################################################################
# Copyright (c) 2023. Samy Ben Dhiab (Samsoucoupe) All rights reserved.        #
#                                                                              #
#  Licensed under the Apache License, Version 2.0 (the "License");             #
#  you may not use this file except in compliance with the License.            #
#  You may obtain a copy of the License at                                     #
#                                                                              #
#       http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                              #
#   Unless required by applicable law or agreed to in writing, software        #
#   distributed under the License is distributed on an "AS IS" BASIS,          #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#   See the License for the specific language governing permissions and        #
#   limitations under the License.                                             #
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
  echo "How many steps do you want to use for the solution ?"
  read max
else
  echo "Enter a name for the rules:"
  read variable
  python3 utils/question.py -f $variable
  python3 utils/generator.py --rulesfiles Rules/Rules_$variable.json --output XML/$variable.xml
  max=$(cat Rules/Rules_$variable.json | grep "solution_max" | cut -d':' -f2 | cut -d',' -f1 | cut -d' ' -f2)
fi

echo "The problem is: $variable"

#nombre de coup max pour la solution


echo "Is it a river problem ? (True or False):"
read river
if [ $river = "True" ] || [ $river = "true" ]
then
  echo "The problem is a river crossing problem"
  utils/genere_solution.sh true $variable $max
else
  echo "The problem is not a river crossing problem"
  utils/genere_solution.sh false $variable $max
fi

utils/Interface/Conclution.sh
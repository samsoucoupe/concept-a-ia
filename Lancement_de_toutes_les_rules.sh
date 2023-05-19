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

list=$(ls Rules)
echo "List of all the rules files:"
echo  $list
for file in $list
#  python3 utils/generator.py --rulesfiles Rules/Rules_$variable.json --output XML/$variable.xml
do
#  Rules_Indien_Americain.json => Indien_Americain
#  enleves les 6 premiers caracteres
  name=$(echo $file |cut -d'.' -f1 | cut -c7-)
  python3 utils/generator.py --rulesfiles Rules/$file --output XML/$name.xml
  #  on ouvre le fichier et on regarde le type de probleme
  #  si c'est un probleme de riviere on lance le programme avec l'option -r true
  #  sinon on lance le programme avec l'option -r false
  #  ouverture du json
  open=$(cat Rules/$file | grep "type" | cut -d':' -f2 | cut -d',' -f1 | cut -d' ' -f2 | cut -d'"' -f2)

  #  nombre de coup max pour la solution
  max=$(cat Rules/$file | grep "solution_max" | cut -d':' -f2 | cut -d',' -f1 | cut -d' ' -f2)
  size=${#max}
  if [ $open = "river" ]
  then
    utils/genere_solution.sh true $name $max
    utils/genere_solution.sh false $name $max
  else
    utils/genere_solution.sh false $name $max
  fi
done



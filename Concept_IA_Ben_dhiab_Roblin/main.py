#
#  Copyright (c) 2023. Samy Ben Dhiab (Samsoucoupe) All rights reserved.
#  #
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#  #
#        http://www.apache.org/licenses/LICENSE-2.0
#  #
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import json
# import
import os

import utils.Affiche_fichier as affiche_fichier
import utils.generator as generator
import utils.genere_solution as genere_solution
import utils.question as question

affiche_fichier.affiche_fichier("utils/Interface/Introduction.txt")

print("Do you want to use the rules in the Rules folder (True or False):")
use = input().lower()
files = os.listdir("Rules")
if use == "true":
    print("List of the rules in the Rules folder:")
    files = os.listdir("Rules")
    print(files)
    print("Enter the name of the file ( For example: Rules_LCS.json => LCS):")
    variable = input()
    while f"Rules_{variable}.json" not in files:
        print("Enter the name of the file ( For example: Rules_LCS.json => LCS):")
        variable = input()
    max_val = json.load(open(f"Rules/Rules_{variable}.json", "r"))["info_problem"]["solution_max"]

else:
    print("List of the rules in the Rules folder:")
    print(files)
    print("Enter a name for the rules:")
    variable = input()
    if variable.startswith("Rules_"):
        variable = variable[6:]
    if f"Rules_{variable}.json" in files:
        print("The name is already used, do you want to overwrite it (True or False):")
        overwrite = input().lower()
        while overwrite not in ["true", "false"]:
            print("The name is already used, do you want to overwrite it (True or False):")
            overwrite = input().lower()
        if overwrite == "false":
            while f"Rules_{variable}.json" in files:
                print("Enter another name for the rules:")
                variable = input()
                if variable.startswith("Rules_"):
                    variable = variable[6:]
    question.questionnaire(variable)
    generator.lauch(f"Rules/Rules_{variable}.json", f"XML/{variable}.xml")
    max_val = json.load(open(f"Rules/Rules_{variable}.json", "r"))["info_problem"]["solution_max"]

print("The problem is:", variable)
if json.load(open(f"Rules/Rules_{variable}.json", "r"))["info_problem"]["type"] == "river":
    genere_solution.solution(variable, max_val, "true")
genere_solution.solution(variable, max_val, "false")

affiche_fichier.affiche_fichier("utils/Interface/Conclusion.txt")

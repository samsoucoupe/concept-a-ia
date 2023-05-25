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

import os
import sys

import dot_solution, converter


def new_rep(name):
    os.makedirs(f"PNG/{name}", exist_ok=True)
    os.makedirs(f"DOT/{name}", exist_ok=True)
    for elt in os.listdir(f"PNG/{name}"):
        if os.path.isfile(f"PNG/{name}/{elt}"):
            os.remove(f"PNG/{name}/{elt}")
    for elt in os.listdir(f"DOT/{name}"):
        if os.path.isfile(f"DOT/{name}/{elt}"):
            os.remove(f"DOT/{name}/{elt}")


def solution(variable, max_val, river):
    if river == "true":
        variable_r = variable + "_River"
        new_rep(variable_r)
        converter.xml_to_dot(f"XML/{variable}.xml", f"DOT/{variable_r}/{variable}.dot", True)
        os.system(
             f"java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n {max_val} -print 0 -resultsType 1 -crossingRiver true -file XML/{variable}.xml")
        os.system(
            f"java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n {max_val} -print 0 -resultsType 1 -crossingRiver false -file XML/{variable}.xml > TXT/{variable_r}.txt")
        dot_solution.lauch(variable, True)
        files = os.listdir(f"DOT/{variable_r}")
        for file in files:
            file_name = os.path.splitext(file)[0]
            os.system(f"dot -Tpng DOT/{variable_r}/{file} -o PNG/{variable_r}/{file_name}.png")
    else:
        new_rep(variable)
        converter.xml_to_dot(f"XML/{variable}.xml", f"DOT/{variable}/{variable}.dot", False)
        os.system(
             f"java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n {max_val} -print 0 -resultsType 1 -crossingRiver false -file XML/{variable}.xml > TXT/{variable}.txt")
        dot_solution.lauch(variable, False)
        files = os.listdir(f"DOT/{variable}")
        for file in files:
            file_name = os.path.splitext(file)[0]
            os.system(f"dot -Tpng DOT/{variable}/{file} -o PNG/{variable}/{file_name}.png")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 genere_solution.py <river_mode> <name> <max_val>")
        exit(1)
    variable = sys.argv[2]
    max_val = sys.argv[3]
    river = sys.argv[1]
    solution(variable, max_val, river)

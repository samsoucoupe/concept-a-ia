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
import os
type_python = input("Type of python (python3 or python): ")

files = os.listdir("Rules")
print("List of all the rules files:")
print(files)
for file in files:
    name = file.split(".")[0][6:]
    os.system(f"{type_python} utils/generator.py --rulesfiles Rules/{file} --output XML/{name}.xml")
    open_type = json.load(open(f"Rules/{file}", "r"))["info_problem"]["type"]
    max_val = json.load(open(f"Rules/{file}", "r"))["info_problem"]["solution_max"]
    if open_type == "river":
        os.system(f"{type_python} utils/genere_solution.py true {name} {max_val}")
        os.system(f"{type_python} utils/genere_solution.py false {name} {max_val}")
    else:
        os.system(f"{type_python} utils/genere_solution.py false {name} {max_val}")

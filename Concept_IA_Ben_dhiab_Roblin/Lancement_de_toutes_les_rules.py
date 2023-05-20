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

files = os.listdir("Rules")
print("List of all the rules files:")
print(files)
for file in files:
    name = file.split(".")[0][6:]
    os.system(f"python3 utils/generator.py --rulesfiles Rules/{file} --output XML/{name}.xml")
    open_type = os.popen(
        f"cat Rules/{file} | grep 'type' | cut -d':' -f2 | cut -d',' -f1 | cut -d' ' -f2 | cut -d'\"' -f2").read().strip()
    max_val = os.popen(
        f"cat Rules/{file} | grep 'solution_max' | cut -d':' -f2 | cut -d',' -f1 | cut -d' ' -f2").read().strip()
    if open_type == "river":
        os.system(f"python3 utils/genere_solution.py true {name} {max_val}")
        os.system(f"python3 utils/genere_solution.py false {name} {max_val}")
    else:
        os.system(f"python3 utils/genere_solution.py false {name} {max_val}")

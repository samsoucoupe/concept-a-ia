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


def affiche_fichier(path):
    with open(path, 'r') as f:
        data = f.readlines()
        for ligne in data:
            if ligne[0] == '#':
                continue
            else:
                print(ligne, end='')


if __name__ == '__main__':
    print("Enter the path of the file:")
    path = input()
    affiche_fichier(path)

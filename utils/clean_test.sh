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

#dans les repertoires DOT,PNG et XML, on clean le repertoire test
#rm -rf ../DOT/test/*
#rm -rf ../PNG/test/*
#rm -rf ../XML/test/*

# si on est dans le repertoire utils (la fin de pwd est utils)
if [[ $PWD == *"java/utils"* ]]; then
    pwd
    cd ..
fi
pwd
# si on est dans le repertoire java (la fin de pwd est java) on clean
if [[ $PWD == *"java"* ]]; then
    rm -rf DOT/test/*
    rm -rf PNG/test/*
    rm -rf XML/test/*
fi

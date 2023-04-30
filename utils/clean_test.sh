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

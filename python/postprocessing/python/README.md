# NANOTop


## find some nanoAODv9

dasgoclient --query="dataset dataset=/*/*UL*NanoAODv9*/NANOAOD*"

dasgoclient --query="dataset dataset=/DoubleMuon/*UL*NanoAODv9*/NANOAOD*"

 dasgoclient --query="file dataset=/DoubleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"

 xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root .

python3 Analysis.py -o test

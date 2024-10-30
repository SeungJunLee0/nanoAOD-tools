# NANOTop

git clone https://github.com/SeungJunLee0/nanoAOD-tools.git  PhysicsTools/NanoAODTools 


cd PhysicsTools/NanoAODTools/python/postprocessing/python

mkdir output



## find some nanoAODv9


dasgoclient --query="dataset dataset=/*/*UL18*NanoAODv9*/NANOAOD*"

dasgoclient --query="dataset dataset=/*/*UL*NanoAODv9*/NANOAOD*"

dasgoclient --query="dataset dataset=/DoubleMuon/*UL*NanoAODv9*/NANOAOD*"

 dasgoclient --query="file dataset=/DoubleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"

 xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root .

python3 Analysis.py -o test


root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C218937D-A2AC-9949-8E65-D14C50F824AF.root
root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C218937D-A2AC-9949-8E65-D14C50F824AF.root






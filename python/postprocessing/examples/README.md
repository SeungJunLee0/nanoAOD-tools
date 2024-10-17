# RDF_NANOTop


## find some nanoAODv9

dasgoclient --query="dataset dataset=/*/*UL*NanoAODv9*/NANOAOD*"
dasgoclient --query="dataset dataset=/DoubleMuon/*UL*NanoAODv9*/NANOAOD*"
dasgoclient --query="file dataset=/DoubleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD"

xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018D/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9_GT36-v1/2820000/1281421E-6BF5-1A4D-BFE6-A97A4088E79C.root .

python3 Analysis.py -o test

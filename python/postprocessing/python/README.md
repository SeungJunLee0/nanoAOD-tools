# DeepTopwidth
## Useful Links:
- [azh_coffe](https://github.com/GageDeZoort/azh_coffea/blob/main/README.md) : markdowon example
- [CMS Physics Object](https://cms-opendata-workshop.github.io/workshop2024-lesson-physics-objects/instructor/06-jecjer.html) : Electron, Muon, Jets, MET, Tagging, Jet correction etc
- [Jet Energy Corrections](https://cms-jerc.web.cern.ch/JEC/#factorized-approach) : Jet Energy Corrections
- [jsonPOG-integration]( https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME) : All of json file
- [B-Tagging eff](https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/) : how to calculate the b_eff
- [Jet energy resolution](https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution#Run2_JER_uncertainty_correlation) : how to calculate the JER
## Quickstart
```

git clone https://github.com/SeungJunLee0/nanoAOD-tools.git  PhysicsTools/NanoAODTools 


cd PhysicsTools/NanoAODTools/python/postprocessing/python

mkdir output

```
### Run the code 
```
python3 set_the_condor_job.py

python3 excute_all.py 
```
### if you want specific dir(specific mc or data)
```
python3 mc_test.py

cd run_~~~~/HTCondor/

bash dashgo.sh
```
### After condor job Merge the output
```
python3 merge_result.py
```

### Find some nanoAODv9

```
dasgoclient --query="dataset dataset=/*/*UL18*NanoAODv9*/NANOAOD*"

dasgoclient --query="dataset dataset=/*/*UL*NanoAODv9*/NANOAOD*"

dasgoclient --query="dataset dataset=/DoubleMuon/*UL*NanoAODv9*/NANOAOD*"

 dasgoclient --query="file dataset=/DoubleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"

 xrdcp root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root .

python3 Analysis.py -o test


root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C218937D-A2AC-9949-8E65-D14C50F824AF.root
root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C218937D-A2AC-9949-8E65-D14C50F824AF.root
```





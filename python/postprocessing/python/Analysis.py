#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from importlib import import_module
#import FWCore.PythonUtilities.LumiList as LumiList
import numpy as np
import os
import sys
import ROOT
import glob
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True




class ExampleAnalysis(Module):
    def __init__(self,  some_variable=None):
        self.writeHistFile = True
        self.some_variable = some_variable  # 전달된 변수 저장

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)


    
        hist_configs = {
            'm_ll': ('m_ll', 'm_{ll}', 300, 0, 100, "", ""),
            'm_muonptarry': ('m_muonptarry', 'Muon_{pt} array', 100, -25, 25, "", ""),
            
            # Zero
            'Zerotag_lep1pt':  ('Zerotag_lep1pt' , 'Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'Zerotag_lep1eta': ('Zerotag_lep1eta', 'Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'Zerotag_jet1eta': ('Zerotag_jet1eta', 'Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'Zerotag_jet1pt':  ('Zerotag_jet1pt' , 'Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'Zerotag_m_ll':    ('Zerotag_m_ll'   , 'Zerotagm_{ll}'   , 300, 0, 100, "", ""),
            'Zerotag_numberofmuon': ('Zerotag_numberofmuon', 'Zerotag_numberofmuon', 10, 0, 10, "", ""),
            
            # Zeromumu
            'mumu_Zerotag_lep1pt':  ('mumu_Zerotag_lep1pt' , 'mumu_Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_lep2pt':  ('mumu_Zerotag_lep2pt' , 'mumu_Zerotag_lep2pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_lep1eta': ('mumu_Zerotag_lep1eta', 'mumu_Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_lep2eta': ('mumu_Zerotag_lep2eta', 'mumu_Zerotag_lep2eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet1eta': ('mumu_Zerotag_jet1eta', 'mumu_Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet2eta': ('mumu_Zerotag_jet2eta', 'mumu_Zerotag_jet2eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet1pt':  ('mumu_Zerotag_jet1pt' , 'mumu_Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_jet2pt':  ('mumu_Zerotag_jet2pt' , 'mumu_Zerotag_jet2pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_m_ll':    ('mumu_Zerotag_m_ll'   , 'mumu_Zerotagm_{ll}'   , 300, 0, 100, "", ""),
            # One
            
            # Two
        }
        
        for attr_name, (hist_name, title, bins, x_min, x_max, x_title, y_title) in hist_configs.items():
            hist = ROOT.TH1F(hist_name, title, bins, x_min, x_max)
            hist.GetXaxis().SetTitle(x_title)
            hist.GetYaxis().SetTitle(y_title)
            self.addObject(hist)
            setattr(self, attr_name, hist)




    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        met = Object(event, "MET")
        hlt = Object(event, "HLT")
        pv = Object(event,"PV")
        #print(self.some_variable)


        if len(jets) <2 or pv.npvs == 0 or pv.ndof < 4 or np.abs(pv.z) >= 24.:
            return False




        hlt_conditions = {
            "mumu_2018": [
                 hlt.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,
            ],
            "single_mu_2018": [
                 hlt.IsoMu24,
            ],
            "single_e_2018": [
                 hlt.Ele32_WPTight_Gsf,
            ],
            "ee_2018": [
                 hlt.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,
                 hlt.DoubleEle25_CaloIdL_MW,
            ],
            "emu_2018": [
                 hlt.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,
                 hlt.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,
            ],
        }

        channel = "None"
        condition_key = ""
        hlt_trigger_results = {}
        for key, triggers in hlt_conditions.items():
            hlt_trigger_results[key] = any(trigger for trigger in triggers)


        if "Data" in self.some_variable and "DoubleMuon" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("mumu_2018", False):
            channel = "mumu"

        elif "Data" in self.some_variable and "SingleMuon" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("mumu_2018", True) and hlt_trigger_results.get("single_mu_2018", False):
            channel = "mumu"


        elif "Data" in self.some_variable and "SingleMuon" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("emu_2018", True) and hlt_trigger_results.get("single_e_2018", True) and hlt_trigger_results.get("single_mu_2018", False):
            channel = "emu"

        elif "Data" in self.some_variable and "SingleElectron" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("emu_2018", True) and hlt_trigger_results.get("single_mu_2018", True) and hlt_trigger_results.get("single_e_2018", False):
            channel = "emu"

        elif "Data" in self.some_variable and "SingleElectron" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("ee_2018", True) and  hlt_trigger_results.get("single_e_2018", False):
            channel = "ee"

        elif "Data" in self.some_variable and "DoubleEG" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("ee_2018", False):
            channel = "ee"

        elif "Data" in self.some_variable and "MuonEG" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("emu_2018", False):
            channel = "emu"


        elif "Data" in self.some_variable and "EGamma" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("ee_2018", False) or hlt_trigger_results.get("single_e_2018", False):
            channel = "ee"

        elif "Data" in self.some_variable and "EGamma" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("emu_2018", True) and hlt_trigger_results.get("single_mu_2018", True) and hlt_trigger_results.get("single_e_2018", False):
            channel = "emu"





        elif "MC" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("ee_2018", False) or hlt_trigger_results.get("single_e_2018", False):
            channel = "ee"



        elif "MC" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("emu_2018", False) or hlt_trigger_results.get("single_e_2018", False) and hlt_trigger_results.get("single_mu_2018", False):
            channel = "emu"

        elif "MC" in self.some_variable and "2018" in self.some_variable and \
            hlt_trigger_results.get("mumu_2018", False) or hlt_trigger_results.get("single_mu_2018", False):
            channel = "mumu"







        if channel == "None":
            return False


        if channel != "emu" and met.pt <=40.0:
            return False



        count_muons =0
        muons_index = []
        for index,l in enumerate(muons):
            if muons[index].pfRelIso04_all < 0.15 and muons[index].tightId and muons[index].pt >20. and muons[index].eta < 2.4:
                count_muons +=1 
                muons_index.append(index)

        count_electrons =0
        electrons_index = []
        for index,l in enumerate(electrons):
            if electrons[index].pt >20. and electrons[index].eta < 2.4:
                count_electrons +=1 
                electrons_index.append(index)


        if channel == "mumu" and count_muons != 2:
            return False

        if channel == "emu" and ( count_muons !=1 or  count_electrons != 1):
            return False

        if channel == "ee" and count_electrons != 2:
            return False


        if channel == "mumu" and count_muons == 2:
            if muons[muons_index[0]].pt <= 25. and muons[muons_index[1]].pt <= 25 :
                return False
        
        if channel == "emu" and count_muons == 1 and  count_electrons == 1:
            if muons[muons_index[0]].pt <= 25. and electrons[electrons_index[0]].pt <= 25:
                return False

        if channel == "ee" and count_electrons == 2:
            if electrons[electrons_index[0]].pt <= 25. and electrons[electrons_index[1]].pt <= 25:
                return False






        if channel =="mumu" and ( (muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M() <= 20 or np.abs((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M() -91.19) <= 15.0):
            return False

        if channel == "ee" and ( (electrons[electrons_index[0]].p4() + electrons[electrons_index[1]].p4()).M() <= 20 or np.abs((electrons[electrons_index[0]].p4() + electrons[electrons_index[1]].p4()).M() -91.19) <15.0):
            return False

        if channel == "emu" and (muons[muons_index[0]].p4() + electrons[electrons_index[0]].p4()).M() <= 20:
            return False



        nBtag =0
        nDeltaR =0
        jet_index = []
        if channel =="mumu":
            for index,j in enumerate(jets):
                if j.pt >30 and np.abs(j.eta) <2.4 and j.jetId > 1:
                    if deltaR(j.eta,j.phi,muons[muons_index[0]].eta,muons[muons_index[0]].phi) > 0.4 and deltaR(j.eta,j.phi,muons[muons_index[1]].eta,muons[muons_index[1]].phi) > 0.4:
                #continue
                        nDeltaR +=1
                        jet_index.append(index) 
                    if deltaR(j.eta,j.phi,muons[muons_index[0]].eta,muons[muons_index[0]].phi) > 0.4 and deltaR(j.eta,j.phi,muons[muons_index[1]].eta,muons[muons_index[1]].phi) > 0.4 and j.btagDeepFlavB > 0.2770:
                        nBtag +=1
            if nBtag ==0 and nDeltaR >=2:
                self.mumu_Zerotag_lep1pt.Fill(muons[muons_index[0]].pt)
                #self.zeromuonseta.Fill(muons[muons_index[0]].eta)
                #self.zerojeteta.Fill(jets[jet_index[0]].eta)
                #self.zerojetpt.Fill(jets[jet_index[0]].pt)

                #self.zerosubmuonspt.Fill(muons[muons_index[1]].pt)
                #self.zerosubmuonseta.Fill(muons[muons_index[1]].eta)
                #self.zerosubjeteta.Fill(jets[jet_index[1]].eta)
                #self.zerosubjetpt.Fill(jets[jet_index[1]].pt)
                #self.num_muon.Fill(len(muons))
                #self.zeromll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
            #if nBtag ==1 and nDeltaR >= 2:
            #    self.h_onemuonspt.Fill(muons[muons_index[0]].pt)
            #    self.h_onemuonseta.Fill(muons[muons_index[0]].eta)
            #    self.h_onejeteta.Fill(jets[jet_index[0]].eta)
            #    self.h_onejetpt.Fill(jets[jet_index[0]].pt)
            #    self.h_onesubmuonspt.Fill(muons[muons_index[1]].pt)
            #    self.h_onesubmuonseta.Fill(muons[muons_index[1]].eta)
            #    self.h_onesubjeteta.Fill(jets[jet_index[1]].eta)
            #    self.h_onesubjetpt.Fill(jets[jet_index[1]].pt)
            #    self.h_onemll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
            #if nBtag ==2 and nDeltaR >= 2:    
            #    self.h_twomuonspt.Fill(muons[muons_index[0]].pt)
            #    self.h_twomuonseta.Fill(muons[muons_index[0]].eta)
            #    self.h_twojeteta.Fill(jets[jet_index[0]].eta)
            #    self.h_twojetpt.Fill(jets[jet_index[0]].pt)
            #    self.h_twosubmuonspt.Fill(muons[muons_index[1]].pt)
            #    self.h_twosubmuonseta.Fill(muons[muons_index[1]].eta)
            #    self.h_twosubjeteta.Fill(jets[jet_index[1]].eta)
            #    self.h_twosubjetpt.Fill(jets[jet_index[1]].pt)
            #    self.h_twomll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
                
          

        return True


def presel():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',type=str, nargs='+', default='root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root')
    #parser.add_argument('-f', '--file',type=str, default=['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/test.root'])
    #parser.add_argument('-f', '--file',type=str, default=['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data.root'])
    parser.add_argument('-n', '--name',type=str, default='what')
    args = parser.parse_args()
    print(str(args.file))
    json ="../data/JSON/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" 
    AllName = "output/hist_" + args.name +".root"
    preselection = "PV_ndof >=4 && PV_npvs != 0 "#"Muon_pt[0] > 25"# && Muon_pt[1] >20" #, "Muon_pt[1] >20" 
    files = args.file
    some_variable = args.name#"My Example Variable"

    if "Data" in args.name:
        print("It is data")
        p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                          ExampleAnalysis(some_variable)],jsonInput=json, noOut=True, histFileName= AllName, histDirName="plots")
        p.run()

    else:
        print("It is MC")
        p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                          ExampleAnalysis(some_variable)], noOut=True, histFileName= AllName, histDirName="plots")
        p.run()



if __name__=="__main__":
    presel()

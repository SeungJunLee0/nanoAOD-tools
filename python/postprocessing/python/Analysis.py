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

        self.h_mbl = ROOT.TH1F('m_lb', 'm_{lb}', 100, 0, 500.)
        self.h_mbl.GetXaxis().SetTitle("Mass GeV/c")
        self.h_mbl.GetYaxis().SetTitle("Number of Events")
        self.addObject(self.h_mbl)


        self.h_mbl2 = ROOT.TH1F('m_lb2', 'm_{lb2}', 100, 0, 500.)
        self.h_mbl2.GetXaxis().SetTitle("Mass GeV/c")
        self.h_mbl2.GetYaxis().SetTitle("Number of Events")
        self.addObject(self.h_mbl2)


        self.h_step = ROOT.TH1F('Step', 'Selection Step', 21, 0, 20)
        self.addObject(self.h_step)
        self.h_mll = ROOT.TH1F('m_ll', 'm_{ll}', 300, 0, 100.)
        self.addObject(self.h_mll)

        self.h_hlt = ROOT.TH1F('m_muonptarry', 'Muon_{pt} array', 100, -25., 25.)
        self.addObject(self.h_hlt)

####################### Zero     
        self.h_zeromuonspt = ROOT.TH1F('Zerotag_muonspt', 'Zerotag_muonspt', 100, 0., 500.)
        self.addObject(self.h_zeromuonspt)

        self.h_zeromuonseta = ROOT.TH1F('Zerotag_muonseta', 'Zerotag_muonseta', 100, -6., 6.)
        self.addObject(self.h_zeromuonseta)

        self.h_zerojeteta = ROOT.TH1F('Zerotag_jeteta', 'Zerotag_jeteta', 100,-6., 6.)
        self.addObject(self.h_zerojeteta)

        self.h_zerojetpt = ROOT.TH1F('Zerotag_jetpt', 'Zerotag_jetpt', 100, 0., 500.)
        self.addObject(self.h_zerojetpt)

        self.h_num_muon = ROOT.TH1F('Zerotag_numberofmuon', 'Zerotag_numberofmuon', 10, 0., 10.)
        self.addObject(self.h_num_muon)

        self.h_zerosubmuonspt = ROOT.TH1F('Zerotag_submuonspt', 'Zerotag_submuonspt', 100, 0., 500.)
        self.addObject(self.h_zerosubmuonspt)

        self.h_zerosubmuonseta = ROOT.TH1F('Zerotag_submuonseta', 'Zerotag_submuonseta', 100, -6., 6.)
        self.addObject(self.h_zerosubmuonseta)

        self.h_zerosubjeteta = ROOT.TH1F('Zerotag_subjeteta', 'Zerotag_subjeteta', 100, -6., 6.)
        self.addObject(self.h_zerosubjeteta)

        self.h_zerosubjetpt = ROOT.TH1F('Zerotag_subjetpt', 'Zerotag_subjetpt', 100, 0., 500.)
        self.addObject(self.h_zerosubjetpt)

        self.h_zeromll = ROOT.TH1F('Zerotag_m_ll', 'Zerotagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_zeromll)

####################### One     
        self.h_onemuonspt = ROOT.TH1F('Onetag_muonspt', 'Onetag_muonspt', 100, 0., 500.)
        self.addObject(self.h_onemuonspt)

        self.h_onemuonseta = ROOT.TH1F('Onetag_muonseta', 'Onetag_muonseta', 100, -6., 6.)
        self.addObject(self.h_onemuonseta)

        self.h_onejeteta = ROOT.TH1F('Onetag_jeteta', 'Onetag_jeteta', 100, -6., 6.)
        self.addObject(self.h_onejeteta)

        self.h_onejetpt = ROOT.TH1F('Onetag_jetpt', 'Onetag_jetpt', 100, 0., 500.)
        self.addObject(self.h_onejetpt)

        self.h_onesubmuonspt = ROOT.TH1F('Onetag_subeptonpt', 'Onetag_submuonspt', 100, 0., 500.)
        self.addObject(self.h_onesubmuonspt)

        self.h_onesubmuonseta = ROOT.TH1F('Onetag_submuonseta', 'Onetag_submuonseta', 100, -6., 6.)
        self.addObject(self.h_onesubmuonseta)

        self.h_onesubjeteta = ROOT.TH1F('Onetag_subjeteta', 'Onetag_subjeteta', 100, -6., 6.)
        self.addObject(self.h_onesubjeteta)

        self.h_onesubjetpt = ROOT.TH1F('Onetag_subjetpt', 'Onetag_subjetpt', 100, 0., 500.)
        self.addObject(self.h_onesubjetpt)

        self.h_onemll = ROOT.TH1F('Onetag_m_ll', 'Onetagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_onemll)

####################### Two     
        self.h_twomuonspt = ROOT.TH1F('Twotag_muonspt', 'Twotag_muonspt', 100, 0., 500.)
        self.addObject(self.h_twomuonspt)                                                                                                 

        self.h_twomuonseta = ROOT.TH1F('Twotag_muonseta', 'Twotag_muonseta', 100, -6., 6.)
        self.addObject(self.h_twomuonseta)
        
        self.h_twojeteta = ROOT.TH1F('Twotag_jeteta', 'Twotag_jeteta', 100, -6., 6.)
        self.addObject(self.h_twojeteta)
    
        self.h_twojetpt = ROOT.TH1F('Twotag_jetpt', 'Twotag_jetpt', 100, 0., 500.)
        self.addObject(self.h_twojetpt)
    
        self.h_twosubmuonspt = ROOT.TH1F('Twotag_subeptonpt', 'Twotag_submuonspt', 100, 0., 500.)
        self.addObject(self.h_twosubmuonspt)
    
        self.h_twosubmuonseta = ROOT.TH1F('Twotag_submuonseta', 'Twotag_submuonseta', 100, -6., 6.)
        self.addObject(self.h_twosubmuonseta)
    
        self.h_twosubjeteta = ROOT.TH1F('Twotag_subjeteta', 'Twotag_subjeteta', 100, -6., 6.)
        self.addObject(self.h_twosubjeteta) 
    
        self.h_twosubjetpt = ROOT.TH1F('Twotag_subjetpt', 'Twotag_subjetpt', 100, 0, 500.)
        self.addObject(self.h_twosubjetpt)                                   

        self.h_twomll = ROOT.TH1F('Twotag_m_ll', 'Twotagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_twomll)


    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        met = Object(event, "MET")
        hlt = Object(event, "HLT")
        pv = Object(event,"PV")
        #print(self.some_variable)


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


        if len(jets) < 2:
            return False
        if pv.npvs == 0 or pv.ndof < 4 or np.abs(pv.z) >= 24.:
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

        if channel == "emu" and (count_muons + count_electrons) != 2:
            return False

        if channel == "ee" and count_electrons != 2:
            return False


        if channel == "mumu" and count_muons == 2:
            if muons[muons_index[0]].pt <= 25. and muons[muons_index[1]].pt <= 25 :
                return False
        
        if channel == "emu" and (count_muons + count_electrons) == 2:
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
                self.h_zeromuonspt.Fill(muons[muons_index[0]].pt)
                self.h_zeromuonseta.Fill(muons[muons_index[0]].eta)
                self.h_zerojeteta.Fill(jets[jet_index[0]].eta)
                self.h_zerojetpt.Fill(jets[jet_index[0]].pt)

                self.h_zerosubmuonspt.Fill(muons[muons_index[1]].pt)
                self.h_zerosubmuonseta.Fill(muons[muons_index[1]].eta)
                self.h_zerosubjeteta.Fill(jets[jet_index[1]].eta)
                self.h_zerosubjetpt.Fill(jets[jet_index[1]].pt)
                self.h_num_muon.Fill(len(muons))
                self.h_zeromll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
            if nBtag ==1 and nDeltaR >= 2:
                self.h_onemuonspt.Fill(muons[muons_index[0]].pt)
                self.h_onemuonseta.Fill(muons[muons_index[0]].eta)
                self.h_onejeteta.Fill(jets[jet_index[0]].eta)
                self.h_onejetpt.Fill(jets[jet_index[0]].pt)
                self.h_onesubmuonspt.Fill(muons[muons_index[1]].pt)
                self.h_onesubmuonseta.Fill(muons[muons_index[1]].eta)
                self.h_onesubjeteta.Fill(jets[jet_index[1]].eta)
                self.h_onesubjetpt.Fill(jets[jet_index[1]].pt)
                self.h_onemll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
            if nBtag ==2 and nDeltaR >= 2:    
                self.h_twomuonspt.Fill(muons[muons_index[0]].pt)
                self.h_twomuonseta.Fill(muons[muons_index[0]].eta)
                self.h_twojeteta.Fill(jets[jet_index[0]].eta)
                self.h_twojetpt.Fill(jets[jet_index[0]].pt)
                self.h_twosubmuonspt.Fill(muons[muons_index[1]].pt)
                self.h_twosubmuonseta.Fill(muons[muons_index[1]].eta)
                self.h_twosubjeteta.Fill(jets[jet_index[1]].eta)
                self.h_twosubjetpt.Fill(jets[jet_index[1]].pt)
                self.h_twomll.Fill((muons[muons_index[0]].p4() + muons[muons_index[1]].p4()).M())
                
          

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

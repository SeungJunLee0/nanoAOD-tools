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
    def __init__(self):
        self.writeHistFile = True

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

     
        self.h_zeroleptonpt = ROOT.TH1F('Zerotag_leptonpt', 'Zerotag_leptonpt', 100, 0., 500.)
        self.addObject(self.h_zeroleptonpt)

        self.h_zeroleptoneta = ROOT.TH1F('Zerotag_leptoneta', 'Zerotag_leptoneta', 100, -6, 6.)
        self.addObject(self.h_zeroleptoneta)

        self.h_zerojeteta = ROOT.TH1F('Zerotag_jeteta', 'Zerotag_jeteta', 100,-6., 6.)
        self.addObject(self.h_zerojeteta)

        self.h_zerojetpt = ROOT.TH1F('Zerotag_jetpt', 'Zerotag_jetpt', 100, 0., 500.)
        self.addObject(self.h_zerojetpt)

        self.h_num_muon = ROOT.TH1F('Zerotag_numberofmuon', 'Zerotag_numberofmuon', 10, 0., 10.)
        self.addObject(self.h_num_muon)





        self.h_zerosubleptonpt = ROOT.TH1F('Zerotag_subeptonpt', 'Zerotag_subleptonpt', 100, 0., 500.)
        self.addObject(self.h_zerosubleptonpt)

        self.h_zerosubleptoneta = ROOT.TH1F('Zerotag_subleptoneta', 'Zerotag_subleptoneta', 100, -6, 6.)
        self.addObject(self.h_zerosubleptoneta)

        self.h_zerosubjeteta = ROOT.TH1F('Zerotag_subjeteta', 'Zerotag_subjeteta', 100, 0., 500.)
        self.addObject(self.h_zerosubjeteta)

        self.h_zerosubjetpt = ROOT.TH1F('Zerotag_subjetpt', 'Zerotag_subjetpt', 100, -6., 6.)
        self.addObject(self.h_zerosubjetpt)


        self.h_oneleptonpt = ROOT.TH1F('Onetag_leptonpt', 'Onetag_leptonpt', 100, 0., 500.)
        self.addObject(self.h_oneleptonpt)

        self.h_oneleptoneta = ROOT.TH1F('Onetag_leptoneta', 'Onetag_leptoneta', 100, -6, 6.)
        self.addObject(self.h_oneleptoneta)

        self.h_onejeteta = ROOT.TH1F('Onetag_jeteta', 'Onetag_jeteta', 100, 0., 500.)
        self.addObject(self.h_onejeteta)

        self.h_onejetpt = ROOT.TH1F('Onetag_jetpt', 'Onetag_jetpt', 100, -6., 6.)
        self.addObject(self.h_onejetpt)


        self.h_onesubleptonpt = ROOT.TH1F('Onetag_subeptonpt', 'Onetag_subleptonpt', 100, 0., 500.)
        self.addObject(self.h_onesubleptonpt)

        self.h_onesubleptoneta = ROOT.TH1F('Onetag_subleptoneta', 'Onetag_subleptoneta', 100, -6, 6.)
        self.addObject(self.h_onesubleptoneta)

        self.h_onesubjeteta = ROOT.TH1F('Onetag_subjeteta', 'Onetag_subjeteta', 100, 0., 500.)
        self.addObject(self.h_onesubjeteta)

        self.h_onesubjetpt = ROOT.TH1F('Onetag_subjetpt', 'Onetag_subjetpt', 100, -6., 6.)
        self.addObject(self.h_onesubjetpt)

        self.h_twoleptonpt = ROOT.TH1F('Twotag_leptonpt', 'Onetag_leptonpt', 100, 0., 500.)
        self.addObject(self.h_twoleptonpt)                                                                                                 
        self.h_twoleptoneta = ROOT.TH1F('Twotag_leptoneta', 'Onetag_leptoneta', 100, -6, 6.)
        self.addObject(self.h_twoleptoneta)
        
        self.h_twojeteta = ROOT.TH1F('Twotag_jeteta', 'Onetag_jeteta', 100, 0., 500.)
        self.addObject(self.h_twojeteta)
    
        self.h_twojetpt = ROOT.TH1F('Twotag_jetpt', 'Onetag_jetpt', 100, -6., 6.)
        self.addObject(self.h_twojetpt)
    
        self.h_twosubleptonpt = ROOT.TH1F('Twotag_subeptonpt', 'Onetag_subleptonpt', 100, 0., 500.)
        self.addObject(self.h_twosubleptonpt)
    
        self.h_twosubleptoneta = ROOT.TH1F('Twotag_subleptoneta', 'Onetag_subleptoneta', 100, -6, 6.)
        self.addObject(self.h_twosubleptoneta)
    
        self.h_twosubjeteta = ROOT.TH1F('Twotag_subjeteta', 'Onetag_subjeteta', 100, 0., 500.)
        self.addObject(self.h_twosubjeteta) 
    
        self.h_twosubjetpt = ROOT.TH1F('Twotag_subjetpt', 'Onetag_subjetpt', 100, -6., 6.)
        self.addObject(self.h_twosubjetpt)                                   


    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        met = Object(event, "MET")
        hlt = Object(event, "HLT")
        pv = Object(event,"PV")
        # select events with at least 2 muons

        #hlt_h = hlt.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or hlt.Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ 
        #hlt_all = hlt.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL or hlt.Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL 
        if len(muons) < 2:
            return False
            #pass
        if met.pt <= 40:
            return False
        if muons[0].pt <= 25 or np.abs(muons[0].eta) >= 2.4:
            return False
        if len(jets) < 2:
            return False
        if jets[0].pt <= 30 or np.abs(jets[0].eta) >=2.4:
            return False
        if pv.npvs == 0 or pv.ndof < 4 or np.abs(pv.z) >= 24.:
            return False
        count_leptons =0
        lepton_index = []
        for index,l in enumerate(muons):
            if muons[index].pfRelIso04_all < 0.15 and muons[index].tightId:
                count_leptons +=1 
                lepton_index.append(index)
        if count_leptons != 2 or muons[lepton_index[0]].charge == muons[lepton_index[1]].charge:
            return False
        nBtag =0
        nDeltaR =0
        jet_index = []
        for index,j in enumerate(jets):
            if j.pt >30 and np.abs(j.eta) <2.4 and j.jetId > 1 and count_leptons == 2:
                if deltaR(j.eta,j.phi,muons[lepton_index[0]].eta,muons[lepton_index[0]].phi) > 0.4 and deltaR(j.eta,j.phi,muons[lepton_index[1]].eta,muons[lepton_index[1]].phi) > 0.4:
                    nDeltaR +=1
                    jet_index.append(index) 
                if j.btagDeepFlavB > 0.2770:
                    nBtag +=1
        if nBtag ==0 and nDeltaR >=2:
            self.h_zeroleptonpt.Fill(muons[lepton_index[0]].pt)
            self.h_zeroleptoneta.Fill(muons[lepton_index[0]].eta)
            self.h_zerojeteta.Fill(jets[jet_index[0]].eta)
            self.h_zerojetpt.Fill(jets[jet_index[0]].pt)

            self.h_zerosubleptonpt.Fill(muons[lepton_index[1]].pt)
            self.h_zerosubleptoneta.Fill(muons[lepton_index[1]].eta)
            self.h_zerosubjeteta.Fill(jets[jet_index[1]].eta)
            self.h_zerosubjetpt.Fill(jets[jet_index[1]].pt)
            self.h_num_muon.Fill(len(muons))
        #if nBtag ==1:
        #if nBtag ==2:    
                
          

        return True

def collectfile(s):
    if s == "test":
        a =['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/RDF_NANOTop/data.root'] 
        return a 
    if s == "c":
        file_list = glob.glob('/store/data/Run2016C/DoubleMuon/NANOAOD/UL2016_MiniAODv1_NanoAODv2-v1/*/*')
    for i in file_list:
        a.append("file:"+str(i))
    
    return a



def presel():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--option',type=str, default='test')
    args = parser.parse_args()
    print(args.option)
    json ="Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt" 
    AllName = "hist_" + args.option +".root"
    preselection = "Muon_pt[0] > 25" , "Muon_pt[1] >20" 
    files = collectfile(args.option) 
    p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                      ExampleAnalysis()], noOut=True, histFileName= AllName, histDirName="plots")
    p.run()

if __name__=="__main__":
    presel()

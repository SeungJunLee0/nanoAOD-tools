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

        self.h_zerosubleptonpt = ROOT.TH1F('Zerotag_subleptonpt', 'Zerotag_subleptonpt', 100, 0., 500.)
        self.addObject(self.h_zerosubleptonpt)

        self.h_zerosubleptoneta = ROOT.TH1F('Zerotag_subleptoneta', 'Zerotag_subleptoneta', 100, -6, 6.)
        self.addObject(self.h_zerosubleptoneta)

        self.h_zerosubjeteta = ROOT.TH1F('Zerotag_subjeteta', 'Zerotag_subjeteta', 100, 0., 500.)
        self.addObject(self.h_zerosubjeteta)

        self.h_zerosubjetpt = ROOT.TH1F('Zerotag_subjetpt', 'Zerotag_subjetpt', 100, -6., 6.)
        self.addObject(self.h_zerosubjetpt)

        self.h_zeromll = ROOT.TH1F('Zerotag_m_ll', 'Zerotagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_zeromll)

####################### One     
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

        self.h_onemll = ROOT.TH1F('Onetag_m_ll', 'Onetagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_onemll)

####################### Two     
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

        self.h_twomll = ROOT.TH1F('Twotag_m_ll', 'Twotagm_{ll}', 300, 0, 100.)
        self.addObject(self.h_twomll)


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
        if muons[0].pt <= 25:
            return False
        if len(jets) < 2:
            return False
        if jets[0].pt <= 30:
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
        if  (muons[lepton_index[0]].p4() + muons[lepton_index[1]].p4()).M() <=20.0 or np.abs((muons[lepton_index[0]].p4() + muons[lepton_index[1]].p4()).M() - 91.19) <=15.0:
            return False

        nBtag =0
        nDeltaR =0
        jet_index = []
        for index,j in enumerate(jets):
            if j.pt >30 and np.abs(j.eta) <2.4 and j.jetId > 1:
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
            self.h_zeromll.Fill((muons[lepton_index[0]].p4() + muons[lepton_index[1]].p4()).M())
        if nBtag ==1 and nDeltaR >= 2:
            self.h_oneleptonpt.Fill(muons[lepton_index[0]].pt)
            self.h_oneleptoneta.Fill(muons[lepton_index[0]].eta)
            self.h_onejeteta.Fill(jets[jet_index[0]].eta)
            self.h_onejetpt.Fill(jets[jet_index[0]].pt)
            self.h_onesubleptonpt.Fill(muons[lepton_index[1]].pt)
            self.h_onesubleptoneta.Fill(muons[lepton_index[1]].eta)
            self.h_onesubjeteta.Fill(jets[jet_index[1]].eta)
            self.h_onesubjetpt.Fill(jets[jet_index[1]].pt)
            self.h_onemll.Fill((muons[lepton_index[0]].p4() + muons[lepton_index[1]].p4()).M())
        if nBtag ==2 and nDeltaR >= 2:    
            self.h_twoleptonpt.Fill(muons[lepton_index[0]].pt)
            self.h_twoleptoneta.Fill(muons[lepton_index[0]].eta)
            self.h_twojeteta.Fill(jets[jet_index[0]].eta)
            self.h_twojetpt.Fill(jets[jet_index[0]].pt)
            self.h_twosubleptonpt.Fill(muons[lepton_index[1]].pt)
            self.h_twosubleptoneta.Fill(muons[lepton_index[1]].eta)
            self.h_twosubjeteta.Fill(jets[jet_index[1]].eta)
            self.h_twosubjetpt.Fill(jets[jet_index[1]].pt)
            self.h_twomll.Fill((muons[lepton_index[0]].p4() + muons[lepton_index[1]].p4()).M())
                
          

        return True


def presel():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',type=str, nargs='+', default='root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root')
    #parser.add_argument('-f', '--file',type=str, default=['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/test.root'])
    #parser.add_argument('-f', '--file',type=str, default=['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data.root'])
    parser.add_argument('-n', '--name',type=str, default='what')
    args = parser.parse_args()
    print(str(args.file))
    json ="Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" 
    AllName = "hist_" + args.name +".root"
    preselection = "Muon_pt[0] > 25"# && Muon_pt[1] >20" #, "Muon_pt[1] >20" 
    files = args.file
    some_variable = "My Example Variable"

    p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                      ExampleAnalysis(some_variable)],jsonInput=json, noOut=True, histFileName= AllName, histDirName="plots")
    p.run()

if __name__=="__main__":
    presel()

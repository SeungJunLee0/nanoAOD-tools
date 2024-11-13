#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from importlib import import_module
from correctionlib import _core
from array import array
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


        # 비균등 bin 설정
        pt_bin_edges = [20, 30, 50, 70, 100, 140, 200, 300, 600, 1000]
        eta_bins = [i * 0.24 for i in range(10 + 1)]  # 0 ~ 2.4를 10개 구간으로 나눔
        flavors = ["b", "c", "light"]  # 제트의 flavor 종류
        
        # 히스토그램을 저장할 딕셔너리
        histograms = {}
        
        # 히스토그램 생성
        for flavor in flavors:
            hist_name = f"{flavor}_all_pt_eta"
            title = f"{flavor}-untagged number of jets; pT; η"
            
            # 2D 히스토그램 생성 및 속성 설정
            hist = ROOT.TH2F(hist_name, title, len(pt_bin_edges) - 1, array('d', pt_bin_edges), len(eta_bins) - 1, array('d', eta_bins))
            hist.GetXaxis().SetTitle("p_{T} [GeV]")
            hist.GetYaxis().SetTitle("|η|")
        
            # 히스토그램을 딕셔너리에 저장
            histograms[hist_name] = hist
            self.addObject(hist)  # 필요한 경우 ROOT 객체로 추가

        # 히스토그램 생성
        for flavor in flavors:
            hist_name = f"{flavor}_tagged_pt_eta"
            title = f"{flavor}-tagged number of jets; pT; η"
            
            # 2D 히스토그램 생성 및 속성 설정
            hist = ROOT.TH2F(hist_name, title, len(pt_bin_edges) - 1, array('d', pt_bin_edges), len(eta_bins) - 1, array('d', eta_bins))
            hist.GetXaxis().SetTitle("p_{T} [GeV]")
            hist.GetYaxis().SetTitle("|η|")
        
            # 히스토그램을 딕셔너리에 저장
            histograms[hist_name] = hist
            self.addObject(hist)  # 필요한 경우 ROOT 객체로 추가


    # Example function to fill histograms based on jet properties
    def fill_histograms(jets):
        for jet in jets:
            # 제트 flavor 결정
            flavor = "b" if jet.hadronFlavour == 5 else "c" if jet.hadronFlavour == 4 else "light"
            
            # pt와 eta 값 가져오기
            pt = jet.pt
            eta = abs(jet.eta)
            
            # 유효한 flavor의 히스토그램에 pt와 eta 값 추가
            hist_name = f"{flavor}_all_eff_pt_eta"
            if hist_name in histograms:
                histograms[hist_name].Fill(pt, eta)

    def fill_histograms_b(jets):
        for jet in jets:
            # 제트 flavor 결정
            flavor = "b" if jet.hadronFlavour == 5 else "c" if jet.hadronFlavour == 4 else "light"
            
            # pt와 eta 값 가져오기
            pt = jet.pt
            eta = abs(jet.eta)
            
            # 유효한 flavor의 히스토그램에 pt와 eta 값 추가
            hist_name = f"{flavor}_tagged_eff_pt_eta"
            if hist_name in histograms:
                histograms[hist_name].Fill(pt, eta)



    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")    
        jets      = Collection(event, "Jet")     
        # get the genWeight value if that is data, genWeight = 1
        met = Object(event, "MET")
        hlt = Object(event, "HLT")
        pv = Object(event,"PV")
        self.count.Fill(1.0,gen_weight)



        
        if pv.npvs == 0 or pv.ndof < 4 or abs(pv.z) >= 24.:
        #primary vertex selection
            return False

        hlt_conditions = {
            "mumu_2018":        hlt.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,
            "single_mu_2018":   hlt.IsoMu24,
            "single_e_2018":    hlt.Ele32_WPTight_Gsf,
            "ee_2018":          ( hlt.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or hlt.DoubleEle25_CaloIdL_MW ),
            "emu_2018":         ( hlt.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or hlt.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL),
        }
        # HLT conditions

        channel = []


        # MC 채널 결정
        if "MC" in self.some_variable and "2018" in self.some_variable:
            if hlt_conditions["ee_2018"] or hlt_conditions["single_e_2018"]:
                channel.append("ee")
            if hlt_conditions["emu_2018"] or hlt_conditions["single_e_2018"] or hlt_conditions["single_mu_2018"]:
                channel.append("emu")
            if hlt_conditions["mumu_2018"] or hlt_conditions["single_mu_2018"]:
                channel.append("mumu")

        # HLT condition check
        if len(channel) == 0:
            return False


        if "ee" in channel and met.pt <=40.0:
            channel.remove("ee")
        if "mumu" in channel and met.pt <=40.0:
            channel.remove("mumu")

        if len(channel) == 0:
            return False

        muons = [m for m in muons if m.pfRelIso04_all < 0.15 and m.tightId and m.pt > 20 and abs(m.eta) < 2.4]
        electrons = [e for e in electrons if e.pt > 20 and abs(e.eta) < 2.4 and e.cutBased >= 4 and ( abs(e.eta +e.deltaEtaSC) < 1.4442 or abs(e.eta +e.deltaEtaSC) > 1.566 )]

        count_muons = len(muons)
        count_electrons = len(electrons)
        
        # Channel conditions
        if "mumu" in channel and ( count_muons != 2 or count_electrons != 0 ):
            channel.remove("mumu")
        
        if "emu" in channel and ( count_muons != 1 or count_electrons != 1):
            channel.remove("emu")
        
        if "ee" in channel and ( count_electrons != 2 or count_muons != 0):
            channel.remove("ee")

        if len(channel) == 0:
            return False
        
        # pt threshold conditions
        if "mumu" in channel and count_muons == 2:
            if muons[0].pt <= 25 and muons[1].pt <= 25:
                channel.remove("mumu")
        
        if "emu" in channel and count_muons == 1 and count_electrons == 1:
            if muons[0].pt <= 25 and electrons[0].pt <= 25:
                channel.remove("emu")
        
        if "ee" in channel and count_electrons == 2:
            if electrons[0].pt <= 25 and electrons[1].pt <= 25:
                channel.remove("ee")

        if len(channel) == 0:
            return False
        
        # Mass conditions
        if "mumu" in channel and ((muons[0].p4() + muons[1].p4()).M() <= 20 or abs((muons[0].p4() + muons[1].p4()).M() - 91.19) <= 15.0):
            channel.remove("mumu")
        
        if "ee" in channel and ((electrons[0].p4() + electrons[1].p4()).M() <= 20 or abs((electrons[0].p4() + electrons[1].p4()).M() - 91.19) <= 15.0):
            channel.remove("ee")
        
        if "emu" in channel and (muons[0].p4() + electrons[0].p4()).M() <= 20:
            channel.remove("emu")

        if len(channel) == 0:
            return False
        muons = sorted(muons, key=lambda x: x.pt, reverse=True)
        electrons = sorted(electrons, key=lambda x: x.pt, reverse=True)

        if "mumu" in channel:
            jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4 and j.jetId >= 1]
            jet_index = [index for index, j in enumerate(jets)
                         if deltaR(j.eta, j.phi, muons[0].eta, muons[0].phi) > 0.4
                         and deltaR(j.eta, j.phi, muons[1].eta, muons[1].phi) > 0.4]
        
            nDeltaR = len(jet_index)
            if  nDeltaR < 2:
                return False
            self.fill_histograms(jets)
            jets = [j for j in jets if j.btagDeepFlavB > 0.2783]
            self.fill_histograms_b(jets)
        


        if "ee" in channel:
            jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4 and j.jetId >= 1]
            jet_index = [index for index, j in enumerate(jets)
                         if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                         and deltaR(j.eta, j.phi, electrons[1].eta, electrons[1].phi) > 0.4]
 
            nDeltaR = len(jet_index)
            if nDeltaR < 2:
                return False
            self.fill_histograms(jets)
            jets = [j for j in jets if j.btagDeepFlavB > 0.2783]
            self.fill_histograms_b(jets)
        
        
        if "emu" in channel:
            jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4 and j.jetId >= 1]
            jet_index = [index for index, j in enumerate(jets)
                         if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                         and deltaR(j.eta, j.phi, muons[0].eta, muons[0].phi) > 0.4]
        
            nDeltaR = len(jet_index)
            if nDeltaR < 2:
                return False
            self.fill_histograms(jets)
            jets = [j for j in jets if j.btagDeepFlavB > 0.2783]
            self.fill_histograms_b(jets)



        return True


def presel():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',type=str, nargs='+', default='root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C489C20E-FD93-8B42-9F63-0AB2FB0F5C39.root')
    #parser.add_argument('-f', '--file',type=str, default=['/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data.root'])
    parser.add_argument('-n', '--name',type=str, default='what')
    args = parser.parse_args()
    print(str(args.file))
    some_variable = args.name
    json ="../data/JSON/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" if "Data" in some_variable else None 
    AllName = "output/hist_" + args.name +".root"
    files = args.file

    if "Data" in args.name:
        print("It is data")

    else:
        print("It is MC")

    p = PostProcessor(".", files, branchsel=None, modules=[
                      ExampleAnalysis(some_variable)],jsonInput=json, noOut=True, histFileName= AllName, histDirName="plots" )
    p.run()


if __name__=="__main__":
    presel()

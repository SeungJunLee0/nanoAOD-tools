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
            'count' :  ('count', 'count', 10, 0, 2, "", ""),
            
            # Zero
            'Zerotag_lep1pt':  ('Zerotag_lep1pt' , 'Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'Zerotag_lep1eta': ('Zerotag_lep1eta', 'Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'Zerotag_jet1eta': ('Zerotag_jet1eta', 'Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'Zerotag_jet1pt':  ('Zerotag_jet1pt' , 'Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'Zerotag_m_ll':    ('Zerotag_m_ll'   , 'Zerotagm_{ll}'   , 300, 0, 100, "", ""),
            'Zerotag_numberofmuon': ('Zerotag_numberofmuon', 'Zerotag_numberofmuon', 10, 0, 10, "", ""),
            # Zero 
            # Zeromumu
            'mumu_Zerotag_MET':     ('mumu_Zerotag_MET'    , 'mumu_Zerotag_MET'     , 100, 0, 500, "", ""),
            'mumu_Zerotag_lep1pt':  ('mumu_Zerotag_lep1pt' , 'mumu_Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_lep2pt':  ('mumu_Zerotag_lep2pt' , 'mumu_Zerotag_lep2pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_lep1eta': ('mumu_Zerotag_lep1eta', 'mumu_Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_lep2eta': ('mumu_Zerotag_lep2eta', 'mumu_Zerotag_lep2eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet1eta': ('mumu_Zerotag_jet1eta', 'mumu_Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet2eta': ('mumu_Zerotag_jet2eta', 'mumu_Zerotag_jet2eta' , 100, -6, 6, "", ""),
            'mumu_Zerotag_jet1pt':  ('mumu_Zerotag_jet1pt' , 'mumu_Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_jet2pt':  ('mumu_Zerotag_jet2pt' , 'mumu_Zerotag_jet2pt'  , 100, 0, 500, "", ""),
            'mumu_Zerotag_m_ll':    ('mumu_Zerotag_m_ll'   , 'mumu_Zerotagm_{ll}'   , 300, 0, 200, "", ""),
            # Zeroemu
            'emu_Zerotag_MET':  ('emu_Zerotag_MET' , 'emu_Zerotag_MET'  , 100, 0, 500, "", ""),
            'emu_Zerotag_lep1pt':  ('emu_Zerotag_lep1pt' , 'emu_Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'emu_Zerotag_lep2pt':  ('emu_Zerotag_lep2pt' , 'emu_Zerotag_lep2pt'  , 100, 0, 500, "", ""),
            'emu_Zerotag_lep1eta': ('emu_Zerotag_lep1eta', 'emu_Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'emu_Zerotag_lep2eta': ('emu_Zerotag_lep2eta', 'emu_Zerotag_lep2eta' , 100, -6, 6, "", ""),
            'emu_Zerotag_jet1eta': ('emu_Zerotag_jet1eta', 'emu_Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'emu_Zerotag_jet2eta': ('emu_Zerotag_jet2eta', 'emu_Zerotag_jet2eta' , 100, -6, 6, "", ""),
            'emu_Zerotag_jet1pt':  ('emu_Zerotag_jet1pt' , 'emu_Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'emu_Zerotag_jet2pt':  ('emu_Zerotag_jet2pt' , 'emu_Zerotag_jet2pt'  , 100, 0, 500, "", ""),
            'emu_Zerotag_m_ll':    ('emu_Zerotag_m_ll'   , 'emu_Zerotagm_{ll}'   , 300, 0, 200, "", ""),
            # Zeroee
            'ee_Zerotag_MET':  ('ee_Zerotag_MET' , 'ee_Zerotag_MET'  , 100, 0, 500, "", ""),
            'ee_Zerotag_lep1pt':  ('ee_Zerotag_lep1pt' , 'ee_Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'ee_Zerotag_lep2pt':  ('ee_Zerotag_lep2pt' , 'ee_Zerotag_lep2pt'  , 100, 0, 500, "", ""),
            'ee_Zerotag_lep1eta': ('ee_Zerotag_lep1eta', 'ee_Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'ee_Zerotag_lep2eta': ('ee_Zerotag_lep2eta', 'ee_Zerotag_lep2eta' , 100, -6, 6, "", ""),
            'ee_Zerotag_jet1eta': ('ee_Zerotag_jet1eta', 'ee_Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'ee_Zerotag_jet2eta': ('ee_Zerotag_jet2eta', 'ee_Zerotag_jet2eta' , 100, -6, 6, "", ""),
            'ee_Zerotag_jet1pt':  ('ee_Zerotag_jet1pt' , 'ee_Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'ee_Zerotag_jet2pt':  ('ee_Zerotag_jet2pt' , 'ee_Zerotag_jet2pt'  , 100, 0, 500, "", ""),
            'ee_Zerotag_m_ll':    ('ee_Zerotag_m_ll'   , 'ee_Zerotagm_{ll}'   , 300, 0, 200, "", ""),
            # Zerocombine
            'combine_Zerotag_MET':  ('combine_Zerotag_MET' , 'combine_Zerotag_MET'  , 100, 0, 500, "", ""),
            'combine_Zerotag_lep1pt':  ('combine_Zerotag_lep1pt' , 'combine_Zerotag_lep1pt'  , 100, 0, 500, "", ""),
            'combine_Zerotag_lep2pt':  ('combine_Zerotag_lep2pt' , 'combine_Zerotag_lep2pt'  , 100, 0, 500, "", ""),
            'combine_Zerotag_lep1eta': ('combine_Zerotag_lep1eta', 'combine_Zerotag_lep1eta' , 100, -6, 6, "", ""),
            'combine_Zerotag_lep2eta': ('combine_Zerotag_lep2eta', 'combine_Zerotag_lep2eta' , 100, -6, 6, "", ""),
            'combine_Zerotag_jet1eta': ('combine_Zerotag_jet1eta', 'combine_Zerotag_jet1eta' , 100, -6, 6, "", ""),
            'combine_Zerotag_jet2eta': ('combine_Zerotag_jet2eta', 'combine_Zerotag_jet2eta' , 100, -6, 6, "", ""),
            'combine_Zerotag_jet1pt':  ('combine_Zerotag_jet1pt' , 'combine_Zerotag_jet1pt'  , 100, 0, 500, "", ""),
            'combine_Zerotag_jet2pt':  ('combine_Zerotag_jet2pt' , 'combine_Zerotag_jet2pt'  , 100, 0, 500, "", ""),
            'combine_Zerotag_m_ll':    ('combine_Zerotag_m_ll'   , 'combine_Zerotagm_{ll}'   , 300, 0, 200, "", ""),
            # One
            # Onemumu
            'mumu_Onetag_MET':  ('mumu_Onetag_MET' , 'mumu_Onetag_MET'  , 100, 0, 500, "", ""),
            'mumu_Onetag_lep1pt':  ('mumu_Onetag_lep1pt' , 'mumu_Onetag_lep1pt'  , 100, 0, 500, "", ""),
            'mumu_Onetag_lep2pt':  ('mumu_Onetag_lep2pt' , 'mumu_Onetag_lep2pt'  , 100, 0, 500, "", ""),
            'mumu_Onetag_lep1eta': ('mumu_Onetag_lep1eta', 'mumu_Onetag_lep1eta' , 100, -6, 6, "", ""),
            'mumu_Onetag_lep2eta': ('mumu_Onetag_lep2eta', 'mumu_Onetag_lep2eta' , 100, -6, 6, "", ""),
            'mumu_Onetag_jet1eta': ('mumu_Onetag_jet1eta', 'mumu_Onetag_jet1eta' , 100, -6, 6, "", ""),
            'mumu_Onetag_jet2eta': ('mumu_Onetag_jet2eta', 'mumu_Onetag_jet2eta' , 100, -6, 6, "", ""),
            'mumu_Onetag_jet1pt':  ('mumu_Onetag_jet1pt' , 'mumu_Onetag_jet1pt'  , 100, 0, 500, "", ""),
            'mumu_Onetag_jet2pt':  ('mumu_Onetag_jet2pt' , 'mumu_Onetag_jet2pt'  , 100, 0, 500, "", ""),
            'mumu_Onetag_m_ll':    ('mumu_Onetag_m_ll'   , 'mumu_Onetagm_{ll}'   , 300, 0, 200, "", ""),
            # Oneemu
            'emu_Onetag_MET':  ('emu_Onetag_MET' , 'emu_Onetag_MET'  , 100, 0, 500, "", ""),
            'emu_Onetag_lep1pt':  ('emu_Onetag_lep1pt' , 'emu_Onetag_lep1pt'  , 100, 0, 500, "", ""),
            'emu_Onetag_lep2pt':  ('emu_Onetag_lep2pt' , 'emu_Onetag_lep2pt'  , 100, 0, 500, "", ""),
            'emu_Onetag_lep1eta': ('emu_Onetag_lep1eta', 'emu_Onetag_lep1eta' , 100, -6, 6, "", ""),
            'emu_Onetag_lep2eta': ('emu_Onetag_lep2eta', 'emu_Onetag_lep2eta' , 100, -6, 6, "", ""),
            'emu_Onetag_jet1eta': ('emu_Onetag_jet1eta', 'emu_Onetag_jet1eta' , 100, -6, 6, "", ""),
            'emu_Onetag_jet2eta': ('emu_Onetag_jet2eta', 'emu_Onetag_jet2eta' , 100, -6, 6, "", ""),
            'emu_Onetag_jet1pt':  ('emu_Onetag_jet1pt' , 'emu_Onetag_jet1pt'  , 100, 0, 500, "", ""),
            'emu_Onetag_jet2pt':  ('emu_Onetag_jet2pt' , 'emu_Onetag_jet2pt'  , 100, 0, 500, "", ""),
            'emu_Onetag_m_ll':    ('emu_Onetag_m_ll'   , 'emu_Onetagm_{ll}'   , 300, 0, 200, "", ""),
            # Oneee
            'ee_Onetag_MET':  ('ee_Onetag_MET' , 'ee_Onetag_MET'  , 100, 0, 500, "", ""),
            'ee_Onetag_lep1pt':  ('ee_Onetag_lep1pt' , 'ee_Onetag_lep1pt'  , 100, 0, 500, "", ""),
            'ee_Onetag_lep2pt':  ('ee_Onetag_lep2pt' , 'ee_Onetag_lep2pt'  , 100, 0, 500, "", ""),
            'ee_Onetag_lep1eta': ('ee_Onetag_lep1eta', 'ee_Onetag_lep1eta' , 100, -6, 6, "", ""),
            'ee_Onetag_lep2eta': ('ee_Onetag_lep2eta', 'ee_Onetag_lep2eta' , 100, -6, 6, "", ""),
            'ee_Onetag_jet1eta': ('ee_Onetag_jet1eta', 'ee_Onetag_jet1eta' , 100, -6, 6, "", ""),
            'ee_Onetag_jet2eta': ('ee_Onetag_jet2eta', 'ee_Onetag_jet2eta' , 100, -6, 6, "", ""),
            'ee_Onetag_jet1pt':  ('ee_Onetag_jet1pt' , 'ee_Onetag_jet1pt'  , 100, 0, 500, "", ""),
            'ee_Onetag_jet2pt':  ('ee_Onetag_jet2pt' , 'ee_Onetag_jet2pt'  , 100, 0, 500, "", ""),
            'ee_Onetag_m_ll':    ('ee_Onetag_m_ll'   , 'ee_Onetagm_{ll}'   , 300, 0, 200, "", ""),
            # Onecombine
            'combine_Onetag_MET':  ('combine_Onetag_MET' , 'combine_Onetag_MET'  , 100, 0, 500, "", ""),
            'combine_Onetag_lep1pt':  ('combine_Onetag_lep1pt' , 'combine_Onetag_lep1pt'  , 100, 0, 500, "", ""),
            'combine_Onetag_lep2pt':  ('combine_Onetag_lep2pt' , 'combine_Onetag_lep2pt'  , 100, 0, 500, "", ""),
            'combine_Onetag_lep1eta': ('combine_Onetag_lep1eta', 'combine_Onetag_lep1eta' , 100, -6, 6, "", ""),
            'combine_Onetag_lep2eta': ('combine_Onetag_lep2eta', 'combine_Onetag_lep2eta' , 100, -6, 6, "", ""),
            'combine_Onetag_jet1eta': ('combine_Onetag_jet1eta', 'combine_Onetag_jet1eta' , 100, -6, 6, "", ""),
            'combine_Onetag_jet2eta': ('combine_Onetag_jet2eta', 'combine_Onetag_jet2eta' , 100, -6, 6, "", ""),
            'combine_Onetag_jet1pt':  ('combine_Onetag_jet1pt' , 'combine_Onetag_jet1pt'  , 100, 0, 500, "", ""),
            'combine_Onetag_jet2pt':  ('combine_Onetag_jet2pt' , 'combine_Onetag_jet2pt'  , 100, 0, 500, "", ""),
            'combine_Onetag_m_ll':    ('combine_Onetag_m_ll'   , 'combine_Onetagm_{ll}'   , 300, 0, 200, "", ""),
            
            # Two
            # Towmumu
            'mumu_Twotag_MET':  ('mumu_Twotag_MET' , 'mumu_Twotag_MET'  , 100, 0, 500, "", ""),
            'mumu_Twotag_lep1pt':  ('mumu_Twotag_lep1pt' , 'mumu_Twotag_lep1pt'  , 100, 0, 500, "", ""),
            'mumu_Twotag_lep2pt':  ('mumu_Twotag_lep2pt' , 'mumu_Twotag_lep2pt'  , 100, 0, 500, "", ""),
            'mumu_Twotag_lep1eta': ('mumu_Twotag_lep1eta', 'mumu_Twotag_lep1eta' , 100, -6, 6, "", ""),
            'mumu_Twotag_lep2eta': ('mumu_Twotag_lep2eta', 'mumu_Twotag_lep2eta' , 100, -6, 6, "", ""),
            'mumu_Twotag_jet1eta': ('mumu_Twotag_jet1eta', 'mumu_Twotag_jet1eta' , 100, -6, 6, "", ""),
            'mumu_Twotag_jet2eta': ('mumu_Twotag_jet2eta', 'mumu_Twotag_jet2eta' , 100, -6, 6, "", ""),
            'mumu_Twotag_jet1pt':  ('mumu_Twotag_jet1pt' , 'mumu_Twotag_jet1pt'  , 100, 0, 500, "", ""),
            'mumu_Twotag_jet2pt':  ('mumu_Twotag_jet2pt' , 'mumu_Twotag_jet2pt'  , 100, 0, 500, "", ""),
            'mumu_Twotag_m_ll':    ('mumu_Twotag_m_ll'   , 'mumu_Twotagm_{ll}'   , 300, 0, 200, "", ""),
            # Twoemu
            'emu_Twotag_MET':  ('emu_Twotag_MET' , 'emu_Twotag_MET'  , 100, 0, 500, "", ""),
            'emu_Twotag_lep1pt':  ('emu_Twotag_lep1pt' , 'emu_Twotag_lep1pt'  , 100, 0, 500, "", ""),
            'emu_Twotag_lep2pt':  ('emu_Twotag_lep2pt' , 'emu_Twotag_lep2pt'  , 100, 0, 500, "", ""),
            'emu_Twotag_lep1eta': ('emu_Twotag_lep1eta', 'emu_Twotag_lep1eta' , 100, -6, 6, "", ""),
            'emu_Twotag_lep2eta': ('emu_Twotag_lep2eta', 'emu_Twotag_lep2eta' , 100, -6, 6, "", ""),
            'emu_Twotag_jet1eta': ('emu_Twotag_jet1eta', 'emu_Twotag_jet1eta' , 100, -6, 6, "", ""),
            'emu_Twotag_jet2eta': ('emu_Twotag_jet2eta', 'emu_Twotag_jet2eta' , 100, -6, 6, "", ""),
            'emu_Twotag_jet1pt':  ('emu_Twotag_jet1pt' , 'emu_Twotag_jet1pt'  , 100, 0, 500, "", ""),
            'emu_Twotag_jet2pt':  ('emu_Twotag_jet2pt' , 'emu_Twotag_jet2pt'  , 100, 0, 500, "", ""),
            'emu_Twotag_m_ll':    ('emu_Twotag_m_ll'   , 'emu_Twotagm_{ll}'   , 300, 0, 200, "", ""),
            # Twoee
            'ee_Twotag_MET':  ('ee_Twotag_MET' , 'ee_Twotag_MET'  , 100, 0, 500, "", ""),
            'ee_Twotag_lep1pt':  ('ee_Twotag_lep1pt' , 'ee_Twotag_lep1pt'  , 100, 0, 500, "", ""),
            'ee_Twotag_lep2pt':  ('ee_Twotag_lep2pt' , 'ee_Twotag_lep2pt'  , 100, 0, 500, "", ""),
            'ee_Twotag_lep1eta': ('ee_Twotag_lep1eta', 'ee_Twotag_lep1eta' , 100, -6, 6, "", ""),
            'ee_Twotag_lep2eta': ('ee_Twotag_lep2eta', 'ee_Twotag_lep2eta' , 100, -6, 6, "", ""),
            'ee_Twotag_jet1eta': ('ee_Twotag_jet1eta', 'ee_Twotag_jet1eta' , 100, -6, 6, "", ""),
            'ee_Twotag_jet2eta': ('ee_Twotag_jet2eta', 'ee_Twotag_jet2eta' , 100, -6, 6, "", ""),
            'ee_Twotag_jet1pt':  ('ee_Twotag_jet1pt' , 'ee_Twotag_jet1pt'  , 100, 0, 500, "", ""),
            'ee_Twotag_jet2pt':  ('ee_Twotag_jet2pt' , 'ee_Twotag_jet2pt'  , 100, 0, 500, "", ""),
            'ee_Twotag_m_ll':    ('ee_Twotag_m_ll'   , 'ee_Twotagm_{ll}'   , 300, 0, 200, "", ""),
            # Twocombine
            'combine_Twotag_MET':  ('combine_Twotag_MET' , 'combine_Twotag_MET'  , 100, 0, 500, "", ""),
            'combine_Twotag_lep1pt':  ('combine_Twotag_lep1pt' , 'combine_Twotag_lep1pt'  , 100, 0, 500, "", ""),
            'combine_Twotag_lep2pt':  ('combine_Twotag_lep2pt' , 'combine_Twotag_lep2pt'  , 100, 0, 500, "", ""),
            'combine_Twotag_lep1eta': ('combine_Twotag_lep1eta', 'combine_Twotag_lep1eta' , 100, -6, 6, "", ""),
            'combine_Twotag_lep2eta': ('combine_Twotag_lep2eta', 'combine_Twotag_lep2eta' , 100, -6, 6, "", ""),
            'combine_Twotag_jet1eta': ('combine_Twotag_jet1eta', 'combine_Twotag_jet1eta' , 100, -6, 6, "", ""),
            'combine_Twotag_jet2eta': ('combine_Twotag_jet2eta', 'combine_Twotag_jet2eta' , 100, -6, 6, "", ""),
            'combine_Twotag_jet1pt':  ('combine_Twotag_jet1pt' , 'combine_Twotag_jet1pt'  , 100, 0, 500, "", ""),
            'combine_Twotag_jet2pt':  ('combine_Twotag_jet2pt' , 'combine_Twotag_jet2pt'  , 100, 0, 500, "", ""),
            'combine_Twotag_m_ll':    ('combine_Twotag_m_ll'   , 'combine_Twotagm_{ll}'   , 300, 0, 200, "", ""),
        }
        
        for attr_name, (hist_name, title, bins, x_min, x_max, x_title, y_title) in hist_configs.items():
            hist = ROOT.TH1F(hist_name, title, bins, x_min, x_max)
            hist.GetXaxis().SetTitle(x_title)
            hist.GetYaxis().SetTitle(y_title)
            self.addObject(hist)
            setattr(self, attr_name, hist)

    def fill_histograms(self, prefix, jets, jet_index, leptons, met, gen_weight):
        getattr(self, f"{prefix}_MET").Fill(met.pt, gen_weight)
        getattr(self, f"{prefix}_lep1pt").Fill(leptons[0].pt, gen_weight)
        getattr(self, f"{prefix}_lep1eta").Fill(leptons[0].eta, gen_weight)
        getattr(self, f"{prefix}_lep2pt").Fill(leptons[1].pt, gen_weight)
        getattr(self, f"{prefix}_lep2eta").Fill(leptons[1].eta, gen_weight)
        getattr(self, f"{prefix}_jet1pt").Fill(jets[jet_index[0]].pt, gen_weight)
        getattr(self, f"{prefix}_jet1eta").Fill(jets[jet_index[0]].eta, gen_weight)
        getattr(self, f"{prefix}_jet2pt").Fill(jets[jet_index[1]].pt, gen_weight)
        getattr(self, f"{prefix}_jet2eta").Fill(jets[jet_index[1]].eta, gen_weight)
        getattr(self, f"{prefix}_m_ll").Fill((leptons[0].p4() + leptons[1].p4()).M(), gen_weight)
    
    def fill_histograms_for_emu(self, prefix, jets, jet_index, electrons, muons, met, gen_weight):
        if electrons[0].pt >= muons[0].pt:
            lep1, lep2 = electrons[0], muons[0]
        else:
            lep1, lep2 = muons[0], electrons[0]

        getattr(self, f"{prefix}_MET").Fill(met.pt, gen_weight)
        getattr(self, f"{prefix}_lep1pt").Fill(lep1.pt, gen_weight)
        getattr(self, f"{prefix}_lep1eta").Fill(lep1.eta, gen_weight)
        getattr(self, f"{prefix}_lep2pt").Fill(lep2.pt, gen_weight)
        getattr(self, f"{prefix}_lep2eta").Fill(lep2.eta, gen_weight)
        getattr(self, f"{prefix}_jet1pt").Fill(jets[jet_index[0]].pt, gen_weight)
        getattr(self, f"{prefix}_jet1eta").Fill(jets[jet_index[0]].eta, gen_weight)
        getattr(self, f"{prefix}_jet2pt").Fill(jets[jet_index[1]].pt, gen_weight)
        getattr(self, f"{prefix}_jet2eta").Fill(jets[jet_index[1]].eta, gen_weight)
        getattr(self, f"{prefix}_m_ll").Fill((lep1.p4() + lep2.p4()).M(), gen_weight)


    def analyze(self, event):
        #electrons = sorted(Collection(event, "Electron"),key=lambda x:x.pt,reverse=True)
        #muons     = sorted(Collection(event, "Muon")    ,key=lambda x:x.pt,reverse=True)
        #jets      = sorted(Collection(event, "Jet")     ,key=lambda x:x.pt,reverse=True)
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")    
        jets      = Collection(event, "Jet")     
        gen_weight = getattr(event, 'genWeight', 1.0) if "MC" in self.some_variable else 1.0
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

        # HLT conditions of Data 
        if "Data" in self.some_variable and "2018" in self.some_variable:
            if "DoubleMuon" in self.some_variable and hlt_conditions["mumu_2018"]:
                channel.append("mumu")
            if "SingleMuon" in self.some_variable:
                if not hlt_conditions["mumu_2018"] and hlt_conditions["single_mu_2018"]:
                    channel.append("mumu")
                if not hlt_conditions["emu_2018"] and not hlt_conditions["single_e_2018"] and hlt_conditions["single_mu_2018"]:
                    channel.append("emu")
            if "SingleElectron" in self.some_variable:
                if not hlt_conditions["emu_2018"] and not hlt_conditions["single_mu_2018"] and hlt_conditions["single_e_2018"]:
                    channel.append("emu")
                if not hlt_conditions["ee_2018"] and hlt_conditions["single_e_2018"]:
                    channel.append("ee")
            if "DoubleEG" in self.some_variable and hlt_conditions["ee_2018"]:
                channel.append("ee")
            if "MuonEG" in self.some_variable and hlt_conditions["emu_2018"]:
                channel.append("emu")
            if "EGamma" in self.some_variable:
                if hlt_conditions["ee_2018"] or hlt_conditions["single_e_2018"]:
                    channel.append("ee")
                if not hlt_conditions["emu_2018"] and not hlt_conditions["single_mu_2018"] and hlt_conditions["single_e_2018"]:
                    channel.append("emu")

        #if "Data" in self.some_variable and "2018" in self.some_variable:
        #    if "DoubleMuon" in self.some_variable and hlt_conditions["mumu_2018"]:
        #        channel.append("mumu")
        #    elif "SingleMuon" in self.some_variable:
        #        if not hlt_conditions["mumu_2018"] and hlt_conditions["single_mu_2018"]:
        #            channel.append("mumu")
        #        elif not hlt_conditions["emu_2018"] and not hlt_conditions["single_e_2018"] and hlt_conditions["single_mu_2018"]:
        #            channel.append("emu")
        #    elif "SingleElectron" in self.some_variable:
        #        if not hlt_conditions["emu_2018"] and not hlt_conditions["single_mu_2018"] and hlt_conditions["single_e_2018"]:
        #            channel.append("emu")
        #        elif not hlt_conditions["ee_2018"] and hlt_conditions["single_e_2018"]:
        #            channel.append("ee")
        #    elif "DoubleEG" in self.some_variable and hlt_conditions["ee_2018"]:
        #        channel.append("ee")
        #    elif "MuonEG" in self.some_variable and hlt_conditions["emu_2018"]:
        #        channel.append("emu")
        #    elif "EGamma" in self.some_variable:
        #        if hlt_conditions["ee_2018"] or hlt_conditions["single_e_2018"]:
        #            channel.append("ee")
        #        elif not hlt_conditions["emu_2018"] and not hlt_conditions["single_mu_2018"] and hlt_conditions["single_e_2018"]:
        #            channel.append("emu")
        #
        # MC 채널 결정
        elif "MC" in self.some_variable and "2018" in self.some_variable:
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
        electrons = [e for e in electrons if e.pt > 20 and abs(e.eta) < 2.4 and e.cutBased >= 4]

        count_muons = len(muons)
        count_electrons = len(electrons)
        
        # Channel conditions
        if "mumu" in channel and ( count_muons != 2 or count_electrons > 0 ):
            channel.remove("mumu")
        
        if "emu" in channel and ( count_muons != 1 or count_electrons != 1):
            channel.remove("emu")
        
        if "ee" in channel and ( count_electrons != 2 or count_muons > 0):
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
            nBtag = sum(1 for j in jets if deltaR(j.eta, j.phi, muons[0].eta, muons[0].phi) > 0.4
                        and deltaR(j.eta, j.phi, muons[1].eta, muons[1].phi) > 0.4
                        and j.btagDeepFlavB > 0.2783)
        
            if nBtag == 0 and nDeltaR >= 2:
                self.fill_histograms("mumu_Zerotag", jets, jet_index, muons, met, gen_weight)
                self.fill_histograms("combine_Zerotag", jets, jet_index, muons, met, gen_weight)
            
            if nBtag == 1 and nDeltaR >= 2:
                self.fill_histograms("mumu_Onetag", jets, jet_index, muons, met, gen_weight)
                self.fill_histograms("combine_Onetag", jets, jet_index, muons, met, gen_weight)
            
            if nBtag == 2 and nDeltaR >= 2:
                self.fill_histograms("mumu_Twotag", jets, jet_index, muons, met, gen_weight)
                self.fill_histograms("combine_Twotag", jets, jet_index, muons, met, gen_weight)
        


        if "ee" in channel:
            jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4 and j.jetId >= 1]
            jet_index = [index for index, j in enumerate(jets)
                         if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                         and deltaR(j.eta, j.phi, electrons[1].eta, electrons[1].phi) > 0.4]
        
            nDeltaR = len(jet_index)
            nBtag = sum(1 for j in jets if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                        and deltaR(j.eta, j.phi, electrons[1].eta, electrons[1].phi) > 0.4
                        and j.btagDeepFlavB > 0.2783)
        
            if nBtag == 0 and nDeltaR >= 2:
                self.fill_histograms("ee_Zerotag", jets, jet_index, electrons, met, gen_weight)
                self.fill_histograms("combine_Zerotag", jets, jet_index, electrons, met, gen_weight)
            
            if nBtag == 1 and nDeltaR >= 2:
                self.fill_histograms("ee_Onetag", jets, jet_index, electrons, met, gen_weight)
                self.fill_histograms("combine_Onetag", jets, jet_index, electrons, met, gen_weight)
            
            if nBtag == 2 and nDeltaR >= 2:
                self.fill_histograms("ee_Twotag", jets, jet_index, electrons, met, gen_weight)
                self.fill_histograms("combine_Twotag", jets, jet_index, electrons, met, gen_weight)
        
        if "emu" in channel:
            jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4 and j.jetId >= 1]
            jet_index = [index for index, j in enumerate(jets)
                         if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                         and deltaR(j.eta, j.phi, muons[0].eta, muons[0].phi) > 0.4]
        
            nDeltaR = len(jet_index)
            nBtag = sum(1 for j in jets if deltaR(j.eta, j.phi, electrons[0].eta, electrons[0].phi) > 0.4
                        and deltaR(j.eta, j.phi, muons[0].eta, muons[0].phi) > 0.4
                        and j.btagDeepFlavB > 0.2783)
        
            if nBtag == 0 and nDeltaR >= 2:
                self.fill_histograms_for_emu("emu_Zerotag", jets, jet_index, electrons,muons, met, gen_weight)
                self.fill_histograms_for_emu("combine_Zerotag", jets, jet_index, electrons,muons, met, gen_weight)

            if nBtag == 1 and nDeltaR >= 2:
                self.fill_histograms_for_emu("emu_Onetag", jets, jet_index, electrons,muons, met, gen_weight)
                self.fill_histograms_for_emu("combine_Onetag", jets, jet_index, electrons,muons, met, gen_weight)
        
            if nBtag == 2 and nDeltaR >= 2:
                self.fill_histograms_for_emu("emu_Twotag", jets, jet_index, electrons,muons, met, gen_weight)
                self.fill_histograms_for_emu("combine_Twotag", jets, jet_index, electrons,muons, met, gen_weight)



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

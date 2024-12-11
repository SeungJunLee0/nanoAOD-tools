#!/usr/bin/env python3
import os
import glob
import random

def get_file_list(directory_path):
    """주어진 디렉토리에서 파일 리스트를 반환합니다."""
    return [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

def main(dir_name):
    print(dir_name[:-4])
    os.system(f"hadd -f output_all/hist_{dir_name[:-4]}.root output_nominal/hist_{dir_name[:-4]}_*")

   

if __name__ == "__main__":
    directory_path = '/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data/'
    file_list = get_file_list(directory_path)
    data_title = file_list

    for dir_name in data_title:
        main(dir_name)
#    os.system(f"hadd -f Data.root hist_DoubleMuon_Data_2018.root hist_EGamma_Data_2018.root hist_MuonEG_Data_2018.root hist_SingleMuon_Data_2018.root")
#    os.system(f"hadd TTbar_signal.root scaled_hist_TTTo2L2Nu_MC_2018.root")
#    os.system(f"hadd TTbar_bkg.root scaled_hist_TTToHadronic_MC_2018.root scaled_hist_TTToSemiLeptonic_MC_2018.root")
#    os.system(f"hadd SingleTop.root scaled_hist_ST_*")
#    os.system(f"hadd WZJets.root scaled_hist_DYJets* hist_WJetsToLNu_MC_2018.root")
#    os.system(f"hadd Diboson.root scaled_hist_WW_MC_2018.root hist_WZ_MC_2018.root hist_ZZ_MC_2018.root")
#    os.system(f"rm -rf hist_*.root")

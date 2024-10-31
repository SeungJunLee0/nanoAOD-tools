#!/usr/bin/env python3
import os
import glob
import random

def get_file_list(directory_path):
    """주어진 디렉토리에서 파일 리스트를 반환합니다."""
    return [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

def main(dir_name):
    print(dir_name[:-4])
    os.system(f"hadd hist_{dir_name[:-4]}.root output/hist_{dir_name[:-4]}_*")
   

if __name__ == "__main__":
    directory_path = '/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data/'
    file_list = get_file_list(directory_path)
    data_title = file_list

    for dir_name in data_title:
        main(dir_name)


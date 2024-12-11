#!/usr/bin/env python3
import os
import glob
import random

def get_file_list(directory_path):
    """주어진 디렉토리에서 파일 리스트를 반환합니다."""
    return [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

def get_file_list_MC(directory_path):
    """주어진 디렉토리에서 파일 리스트를 반환합니다."""
    return [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file)) and "MC" in file]

def select_dir(data_title):
    """데이터 제목 리스트에서 사용자가 선택한 파일을 반환합니다."""
    print("모드를 선택하세요.")
    for idx, title in enumerate(data_title):
        print(f"{title} : {idx}")

    try:
        choice = int(input("파일 번호를 입력하세요: "))
        return data_title[choice]
    except (ValueError, IndexError):
        print("잘못된 입력입니다.")
        return None

def count_text_file(file_path):
    """텍스트 파일의 줄 수를 반환합니다."""
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return []

def get_shell_script(dataset_name, job_id, work_dir, output_dir, dir_name):
    """각 작업에 대해 실행할 셸 스크립트를 생성합니다."""
    script = f"""#!/bin/bash

cat <<'EndOfMCGenerationFile' > MC_Generation_Script_{job_id}.sh
#!/bin/bash

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11

echo "Processing job number {job_id} ... "
export X509_USER_PROXY={work_dir}/x509up
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src
eval `scram runtime -sh`
cmsenv
scram b
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python

python3 Analysis.py -f {dataset_name} -n {dir_name}_{job_id} -c nominal -t nominal
#xrdcp -f output_nominal/hist_{dir_name}_{job_id}_nominal_nominal.root {output_dir}/
EndOfMCGenerationFile

chmod +x MC_Generation_Script_{job_id}.sh
"""
    return script


def get_shell_script_MC(dataset_name, job_id, work_dir, output_dir, dir_name,correction,target):
    """각 작업에 대해 실행할 셸 스크립트를 생성합니다."""
    script = f"""#!/bin/bash

cat <<'EndOfMCGenerationFile' > MC_Generation_Script_{job_id}.sh
#!/bin/bash

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11

echo "Processing job number {job_id} ... "
export X509_USER_PROXY={work_dir}/x509up
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src
eval `scram runtime -sh`
cmsenv
scram b
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python

python3 Analysis.py -f {dataset_name} -n {dir_name}_{job_id} -c {correction} -t {target} 
#xrdcp -f output_correction/hist_{dir_name}_{job_id}_{correction}_{target}.root {output_dir}/
EndOfMCGenerationFile

chmod +x MC_Generation_Script_{job_id}.sh
"""
    return script
def get_condor_submit_file(script_name, work_dir, job_num):
    """HTCondor 제출 파일을 생성합니다."""
    file = f"""RequestMemory         = 9 GB
RequestDisk           = 12 GB
universe              = vanilla
getenv                = True
should_transfer_files = YES
executable            = {script_name}_{job_num}.sh
output                = {script_name}_{job_num}.out
error                 = {script_name}_{job_num}.err
log                   = {script_name}_{job_num}.log
transfer_executable   = True
x509userproxy         = {work_dir}/x509up
queue 1
"""
    return file

def setup_directories(work_dir, run_dir):
    """작업 디렉토리를 설정합니다."""
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(run_dir, exist_ok=True)
    #os.system(f"voms-proxy-init --voms cms -valid 192:00 --out {work_dir}/x509up")
    os.system(f"cp -r /cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/x509up {work_dir}/x509up")

def main(dir_name, choice,correction="nominal",target="nominal"):
    """메인 함수로 작업을 설정하고 작업 스크립트와 제출 파일을 생성합니다."""
    work_dir = f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_{dir_name[:-4]}"
    if choice == "1": # Data
        pass
    if choice == "2": # MC
        pass
    if choice == "3": # Correction
        work_dir += f"_{correction}_{target}" 
    if choice == "4": # B-Tagging
        work_dir += "_B-Tagging" 
    run_dir = f"{work_dir}/HTCondor_run"
    output_dir = f"root://cms-xrdr.private.lo:2094//xrd/store/user/seungjun/TMW/{dir_name[:-4]}"
    if choice == "3": # Correction
        output_dir += f"_{correction}_{target}" 
    if choice == "4": # B-Tagging
        output_dir += "_B-Tagging" 

    setup_directories(work_dir, run_dir)

    njob = count_text_file(f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data/{dir_name}")
    for job_id, dataset_name in enumerate(njob):
        dataset_name = dataset_name.strip()
        with open(f'{run_dir}/mc_generation_job_{job_id}.sh', 'w') as bash_file:
            if choice == "1" or choice =="2":
                bash_file.write(get_shell_script(dataset_name, job_id, work_dir, output_dir, dir_name[:-4]))
            if choice == "3":
                bash_file.write(get_shell_script_MC(dataset_name, job_id, work_dir, output_dir, dir_name[:-4],correction,target))

    for job_id in range(len(njob)):
        job_name = f"{job_id:04}"
        script_name = f"{run_dir}/MC_Generation_Script"
        with open(f'{run_dir}/mc_generation_jobs_{job_name}.submit', 'w') as file_out:
            file_out.write(get_condor_submit_file(script_name, work_dir, job_id))

def mc_to_MC(dir_name,correction="nominal",target="nominal"):
    """생성된 모든 셸 스크립트를 순차적으로 실행합니다."""
    if correction == "nominal" and target== "nominal":
        run_dir = f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_{dir_name[:-4]}/HTCondor_run"
    if correction != "nominal" or target != "nominal":
        run_dir = f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_{dir_name[:-4]}_{correction}_{target}/HTCondor_run"
    os.chdir(run_dir)
    all_scripts = sorted([f for f in glob.glob('mc*.sh') if os.path.isfile(f)])
    
    for script in all_scripts:
        os.system(f"bash {script}")
        os.system("cp -r ../../dashgo.sh .")

if __name__ == "__main__":
    print("원하는 작업을 선택하세요:")
    print("1: Data & MC")
    print("2: MC")
    print("3: Correction")
    print("4: B-Tagging Efficiency")
    choice = input("선택 번호를 입력하세요: ")
    
    os.system(f"voms-proxy-init --voms cms -valid 192:00 --out /cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/x509up")
    directory_path = '/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/data/'
    file_list = get_file_list(directory_path) if  choice == "1" else get_file_list_MC(directory_path)
    data_title = file_list

    correction_sets = ["muon_id", "muon_iso", "electron_id", "electron_reco", "jet_jer", "plieup"]
    mode_dict = {key: "nominal" for key in correction_sets}
    modes = ["up", "down"]

    for dir_name in data_title:
        if choice != "3":
            main(dir_name,choice)
            mc_to_MC(dir_name)
        if choice == "3":
            for target_switch in correction_sets:
                for mode in modes:
                    # 모든 스위치를 "nominal"로 설정
                    mode_dict = {key: "nominal" for key in correction_sets}
                    # 특정 스위치만 현재 mode로 설정
                    mode_dict[target_switch] = mode
                    main(dir_name, choice,correction=target_switch,target=mode)
                    mc_to_MC(dir_name,correction=target_switch,target=mode)

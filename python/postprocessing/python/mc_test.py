#!/usr/bin/env python3                                                                                                                                                             
import os
import sys
import time
import glob
import json
import random
from argparse import ArgumentParser


#data_title = ["test.txt"]
data_title = ["DoubleMuon_data_2018.txt"]

print("press the mode")
for i in range(len(data_title)):
    line_print = data_title[i] + " : " + str(i)
    print(line_print)

x = input()
x = int(x)
line_print = "You choose the "+ data_title[x]
print(line_print)
dir_name = data_title[x]

voms_dir = f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_"+dir_name[:-4]
work_dir = f"/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_"+dir_name[:-4]
run_dir = f"{work_dir}/HTCondor_run"
input_dir =  f"root://cms-xrdr.private.lo:2094//xrd/store/user/seungjun/TMW/"+dir_name[:-4]
output_dir = f"root://cms-xrdr.private.lo:2094//xrd/store/user/seungjun/TMW/"+dir_name[:-4]


def count_text_file(file_path):
    try:
        # 파일 열기
        with open(file_path, 'r') as file:
            # 파일 내용 한 줄씩 읽기
            lines = file.readlines()  # 파일의 모든 줄을 읽어서 리스트로 반환
            #print("Number of lines:", len(lines))  # 줄 수 출력
            return lines
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_text_file(file_path):
    try:
        # 파일 열기
        with open(file_path, 'r') as file:
            # 파일 내용 한 줄씩 읽기
            lines = file.readlines()  # 파일의 모든 줄을 읽어서 리스트로 반환
            print("Number of lines:", len(lines))  # 줄 수 출력
            for line in lines:
                print("['"+line.strip()+"']")  # 각 줄을 출력 (strip()은 줄 끝의 개행 문자를 제거)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def get_shell_script(dataset_name,  job_id, dir_name):
####################################################################################

    script=''
    script+=f'''#!/bin/bash

#source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh

# Dump all code into 'MC_Generation_Script_{job_id}.sh'
cat <<'EndOfMCGenerationFile' > MC_Generation_Script_{job_id}.sh
#!/bin/bash

### Job configuration ###
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11
echo "Processing job number {job_id} ... "
export X509_USER_PROXY={work_dir}/x509up
CWD=`pwd -P`
#mkdir -p /cms/ldap_home/seungjun/{dir_name}/job_{job_id}
#cd /cms/ldap_home/seungjun/{dir_name}/job_{job_id}
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src
#cd $_CONDOR_SCRATCH_DIR
#mkdir -p {dir_name}/job_{job_id}
##
#cd {dir_name}/job_{job_id}
#
#if [ -r CMSSW_13_0_10/src ] ; then
#  echo release CMSSW_13_0_10 already exists
#else
#  scram p CMSSW CMSSW_13_0_10
#fi
#cd CMSSW_13_0_10/src
#git clone https://github.com/SeungJunLee0/nanoAOD-tools.git PhysicsTools/NanoAODTools
eval `scram runtime -sh`
cmsenv
scram b
cd /cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python
python3 Analysis.py -f {dataset_name} -n {dir_name}_{job_id} 
xrdcp -f hist_{dir_name}_{job_id}.root {output_dir}/
EndOfMCGenerationFile

# Make file executable
chmod +x MC_Generation_Script_{job_id}.sh


'''

    return script


def get_condor_submit_file(work_dir,run_dir, nJobs,job_num):
####################################################################################

    script_name = run_dir + "/MC_Generation_Script"

    file=''
    file+=f'RequestMemory         = 9 GB\n'
    file+=f'RequestDisk           = 12 GB\n'
    file+=f'universe              = vanilla\n'
    #file+=f'universe              = container\n'
    #file+=f'container_image       =/cms/container_images/boost.sif\n'
    #file+=f'+SingularityBind =  "/cvmfs,/cms,/cms_scratch,/etc/profile.d"\n'
    file+=f'getenv                = True\n'
    file+=f'should_transfer_files = YES\n'
    file+=f'executable            = {script_name}_{job_num}.sh\n'
    file+=f'output                = {script_name}_{job_num}.out\n'
    file+=f'error                 = {script_name}_{job_num}.err\n'
    file+=f'log                   = {script_name}_{job_num}.log\n'
    file+=f'transfer_executable   = True\n'
    file+=f'x509userproxy = {work_dir}/x509up\n'
    file+=f'queue 1\n'
    file+=f'#\n'

    return file






def main():
####################################################################################
    #njob = count_text_file(dir_name)
    #print(len(njob))
    #parser = ArgumentParser(description="Generate MC Events")
    #parser.add_argument("--nEvent", type=int, default=-1, required=False, help="number of events per job (nTot_dataset = nEvent x nJob)")
    #args = parser.parse_args()

    if(not os.path.exists(work_dir)):
        os.system(f"mkdir {work_dir}")
    else:
        os.system(f"rm -rf {work_dir}/*")

    os.system(f"voms-proxy-init --voms cms -valid 192:00 --out {work_dir}/x509up")


    if(not os.path.exists(run_dir)):
        os.system(f"mkdir {run_dir}")
    else:
        os.system(f"rm -rf {run_dir}/*")


    job_id=0
    njob = count_text_file("data/"+dir_name)
    for iJob in range(len(njob)):
        with open(f'{run_dir}/mc_generation_job_{str(job_id)}.sh','w') as bash_file:  
            bash_file.write(get_shell_script(njob[i].strip() , job_id,dir_name[:-4]))
        job_id+=1


    job_id=0
    for i_num in range(len(njob)):
        job_name = "0000"
        if job_id < 10:                        job_name ="000"+str(job_id)
        if job_id >= 10 and job_id < 100:       job_name ="00"+str(job_id)
        if job_id >= 100 and job_id < 1000:     job_name ="0"+str(job_id)
        if job_id >= 1000 and job_id < 10000:     job_name =str(job_id)


        with open(f'{run_dir}/mc_generation_jobs_{job_name}.submit','w') as file_out:
            file_out.write(get_condor_submit_file(work_dir,run_dir, job_id,job_id))
        job_id+=1


def mc_to_MC():
    os.chdir('/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/run_analysis_'+dir_name[:-4] +'/HTCondor_run/')
    all_folder = glob.glob('mc*.sh')
    all_file = [x for x in all_folder if os.path.isfile(x)]
    all_file.sort()

    for i,file_name in enumerate(all_file):
        command_line = "bash " + file_name
        os.system(command_line)
        os.system("cp -r ../../dashgo.sh .")


if __name__ == "__main__":
    main()
    mc_to_MC()
    ## how am i

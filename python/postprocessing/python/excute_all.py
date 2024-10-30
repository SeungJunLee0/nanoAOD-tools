import os
import glob

def execute_all_dashgo(base_directory):
    # 모든 하위 디렉토리에서 dashgo.sh 파일 찾기
    all_dashgo_scripts = glob.glob(f"{base_directory}/**/HTCondor_run/dashgo.sh", recursive=True)
    
    # 찾은 dashgo.sh 파일 순차적으로 실행
    for dashgo_script in all_dashgo_scripts:
        script_directory = os.path.dirname(dashgo_script)  # dashgo.sh가 위치한 디렉토리 경로
        print(f"Executing: {dashgo_script} in directory {script_directory}")
        
        # 해당 디렉토리로 이동하여 dashgo.sh 실행
        os.chdir(script_directory)
        os.system("bash dashgo.sh")

# 메인 실행 부분
if __name__ == "__main__":
    # run_analysis_~~~ 디렉토리가 위치한 기본 경로를 지정하세요
    base_directory = "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python"
    
    # 모든 dashgo.sh 스크립트 실행
    execute_all_dashgo(base_directory)


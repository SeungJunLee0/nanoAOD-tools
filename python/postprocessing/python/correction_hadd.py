## 기준 디렉토리 설정
#base_dir = "output_correction1"
#
## Correction 및 Target 설정
#corrections = ["muon_id", "muon_iso", "electron_id", "electron_reco", "jet_jer", "plieup"]
#targets = ["up", "down"]
#
## 작업 디렉토리 설정
##os.chdir(base_dir)
#
## 파일 합치기
#for correction in corrections:
#    for target in targets:
#        # 출력 파일 이름 정의
#        output_file = f"output_all/{correction}_{target}.root"
#
#        # 매칭되는 파일 패턴
#        input_pattern = f"output_correction1/*{correction}_{target}.root"
#
#        cmd = f"hadd {output_file} {input_pattern}"
#        print(f"Running command: {cmd}")
#        status = os.system(cmd)
#
#        # 상태 확인
#        if status != 0:
#            print(f"Error occurred while running: {cmd}")
#        # `hadd` 명령어 실행
#        #try:
#        #    print(f"Running hadd for: {output_file}")
#        #    subprocess.run(["hadd", output_file, input_pattern], check=True)
#        #except subprocess.CalledProcessError as e:
#        #    print(f"Error while running hadd for {output_file}: {e}")
import os
import glob
import subprocess

# 기준 디렉토리 및 출력 디렉토리 설정
base_dir = "output_correction1"
output_dir = "output_mid_correction"
os.makedirs(output_dir, exist_ok=True)

# Correction 및 Target 설정
corrections = ["muon_id", "muon_iso", "electron_id", "electron_reco", "jet_jer", "plieup"]
targets = ["up", "down"]

# 스케일 팩터를 결정하는 함수 (파일 이름에 따라 스케일 결정)
def get_scale_factor(filename):
    # 예시 로직: 파일명에 따라 다른 스케일 적용
    # WZJets 관련 파일이면 1.2를 곱한다.
    # Diboson 관련 파일이면 0.8을 곱한다.
    # 기타는 1.0
    setting = 59.6*1000
    if "DYJetsToLL_M-50" in filename:
        return setting * 6077.22
    elif "DYJetsToLL_M-10" in filename:
        return 59.6* 1000 * 18610
    elif "DYJetsToLL_M-10" in filename:
    	return 59.6* 1000 * 18610
    elif "ST_s-channel" in filename:
    	return 59.6* 1000 * 3.36
    elif "ST_t-channel_antitop" in filename:
    	return 59.6* 1000 * 80.95 
    elif "ST_t-channel_top_MC" in filename:
    	return 59.6* 1000 * 136.02
    elif "ST_tW_antitop_MC" in filename:
    	return 59.6* 1000 *34.91 
    elif "ST_tW_top_MC" in filename:
    	return 59.6* 1000 *34.97 
    elif "TTTo2L2Nu_MC_2018" in filename:
    	return 59.6* 1000 * 87.4
    elif "TTToHadronic_MC_2018" in filename:
    	return 59.6* 1000 * 380
    elif "TTToSemiLeptonic_MC" in filename:
    	return 59.6* 1000 * 364
    elif "WJetsToLNu_MC" in filename:
    	return 59.6* 1000 *61526.7 
    elif "WW_MC_2018" in filename:
    	return 59.6* 1000 *118.7 
    elif "WZ_MC_2018" in filename:
    	return 59.6* 1000 * 47.13 
    elif "ZZ_MC_2018" in filename:
    	return 59.6* 1000 *16.523 
    #elif "" in filename:
    #	return 59.6* 1000 * 
    #elif "" in filename:
    #	return 59.6* 1000 * 
    else:
        return 1.0

# 파일 합치기
for correction in corrections:
    for target in targets:
        output_file = f"{output_dir}/{correction}_{target}.root"
        input_pattern = f"{base_dir}/*{correction}_{target}.root"

        # glob으로 입력 파일 리스트 얻기
        input_files = glob.glob(input_pattern)

        if not input_files:
            print(f"No files matched for pattern: {input_pattern}")
            continue

        # hadd 명령어 준비
        cmd = ["hadd", output_file]
        for f in input_files:
            scale = get_scale_factor(f)
            if scale != 1.0:
                # 파일 뒤에 스케일값 추가
                cmd.extend([f, str(scale)])
                print(cmd.extend([f, str(scale)]))
            else:
                cmd.append(f)

        print("Running command:", " ".join(cmd))
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(f"Successfully created {output_file}")


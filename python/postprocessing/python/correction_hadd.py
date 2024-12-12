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
setting = 59.6 * 1000
scale_factors = {
    "DYJetsToLL_M-50": setting * 6077.22,
    "DYJetsToLL_M-10": setting * 18610,
    "ST_s-channel": setting * 3.36,
    "ST_t-channel_antitop": setting * 80.95,
    "ST_t-channel_top_MC": setting * 136.02,
    "ST_tW_antitop_MC": setting * 34.91,
    "ST_tW_top_MC": setting * 34.97,
    "TTTo2L2Nu_MC_2018": setting * 87.4,
    "TTToHadronic_MC_2018": setting * 380,
    "TTToSemiLeptonic_MC": setting * 364,
    "WJetsToLNu_MC": setting * 61526.7,
    "WW_MC_2018": setting * 118.7,
    "WZ_MC_2018": setting * 47.13,
    "ZZ_MC_2018": setting * 16.523
}


# 스케일 팩터를 결정하는 함수 (파일 이름에 따라 스케일 결정)
def get_scale_factor(filename):
    for pattern, factor in scale_factors.items():
        if pattern in filename:
            return factor
    # 매칭되는 패턴이 없으면 1.0 반환
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


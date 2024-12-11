import os
import subprocess

# 기준 디렉토리 설정
base_dir = "output_correction1"

# Correction 및 Target 설정
corrections = ["muon_id", "muon_iso", "electron_id", "electron_reco", "jet_jer", "plieup"]
targets = ["up", "down"]

# 작업 디렉토리 설정
#os.chdir(base_dir)

# 파일 합치기
for correction in corrections:
    for target in targets:
        # 출력 파일 이름 정의
        output_file = f"output_all/{correction}_{target}.root"

        # 매칭되는 파일 패턴
        input_pattern = f"output_correction1/*{correction}_{target}.root"

        cmd = f"hadd {output_file} {input_pattern}"
        print(f"Running command: {cmd}")
        status = os.system(cmd)

        # 상태 확인
        if status != 0:
            print(f"Error occurred while running: {cmd}")
        # `hadd` 명령어 실행
        #try:
        #    print(f"Running hadd for: {output_file}")
        #    subprocess.run(["hadd", output_file, input_pattern], check=True)
        #except subprocess.CalledProcessError as e:
        #    print(f"Error while running hadd for {output_file}: {e}")

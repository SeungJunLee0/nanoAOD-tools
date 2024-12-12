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
import ROOT

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
def get_total_entries(file_path):
    # ROOT 파일 열기
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        raise RuntimeError(f"Error: Cannot open file: {file_path}")

    # 'plots/count' 히스토그램 가져오기
    hist = file.Get("plots/count")
    if not hist or not isinstance(hist, ROOT.TH1):
        raise RuntimeError(f"Error: 'plots/count' histogram not found or is not a TH1 in file: {file_path}")

    # 총 엔트리 수 가져오기
    total_entries = hist.Integral()
    #total_entries = hist.GetEntries()
    file.Close()
    return total_entries

def scale_histograms_in_file(file_path, cross_section):
    file = ROOT.TFile.Open(file_path)

    if not file or file.IsZombie():
        print(f"Error: Cannot open file: {file_path}")
        return None

    # 스케일 팩터 계산 (데이터 파일의 경우 None)
    scale_factor = None
    if cross_section is not None:
        scale_factor = luminosity * 1000 * cross_section

    plots_dir = file.Get("plots")
    if not plots_dir or not isinstance(plots_dir, ROOT.TDirectory):
        print(f"Error: 'plots' directory not found in the file: {file_path}")
        file.Close()
        return None

    # 새 파일에 저장할 히스토그램 목록
    histograms = []
    for key in plots_dir.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TH1):  # 히스토그램일 경우만 처리
            if scale_factor and cross_section >= 2:
                obj.Scale(scale_factor / get_total_entries(file_path) )
                new_entries = obj.Integral()
                obj.SetEntries(new_entries)
                #obj.Scale(scale_factor / obj.GetEntries() if obj.GetEntries() > 0 else 1)
            cloned_hist = obj.Clone()
            cloned_hist.SetDirectory(0)  # 히스토그램을 메모리에 유지
            histograms.append(cloned_hist)

    file.Close()
    return histograms

# 스케일 팩터를 결정하는 함수 (파일 이름에 따라 스케일 결정)
def get_scale_factor(filename):
    for pattern, factor in scale_factors.items():
        if pattern in filename:
            return factor
    # 매칭되는 패턴이 없으면 1.0 반환
    return 1.0

#os.system("rm -rf output_mid_correction/*")
## 파일 합치기
#for pattern in scale_factors.keys():
#    for correction in corrections:
#        for target in targets:
#            output_file = f"{output_dir}/Notscale_{pattern}_{correction}_{target}.root"
#            input_pattern = f"{base_dir}/*{pattern}*{correction}_{target}.root"
#    
#            # glob으로 입력 파일 리스트 얻기
#            print(    f"hadd {output_file} {input_pattern}")
#            os.system(f"hadd {output_file} {input_pattern}")
#    
#    
for pattern in scale_factors.keys():
    for correction in corrections:
        for target in targets:
            output_file = f"{output_dir}/{pattern}_{correction}_{target}.root"
            input_pattern = f"{output_dir}/Notscale_{pattern}_{correction}_{target}.root"
    
            # glob으로 입력 파일 리스트 얻기
            input_files = glob.glob(input_pattern)
            scale = get_scale_factor(input_files) / get_total_entries(input_files)
            print(    f"hadd {output_file} {input_pattern} {scale}")
            os.system(f"hadd {output_file} {input_pattern} {scale}")
    
            if not input_files:
                print(f"No files matched for pattern: {input_pattern}")
                continue

    
            ## hadd 명령어 준비
            #cmd = ["hadd", output_file]
            #for f in input_files:
            #    cmd.append(f)
            #    #scale = get_scale_factor(f) / get_total_entries(f) 
            #    #if scale != 1.0:
            #    #    # 파일 뒤에 스케일값 추가
            #    #    cmd.extend([f, str(scale)])
            #    #    #print(cmd.extend([f, str(scale)]))
            #    #    print("CMD after extending:", cmd)
            #    #else:
            #    #    cmd.append(f)
    
            #print("Running command:", " ".join(cmd))
            #result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
            #if result.returncode != 0:
            #    print(f"Error: {result.stderr}")
            #else:
            #    print(f"Successfully created {output_file}")
    

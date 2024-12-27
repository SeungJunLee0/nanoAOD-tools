import ROOT
import os

def merge_histograms_by_pattern(file_dir, file_pattern, dir_name, hist_pattern, output_file):
    """
    특정 구문을 포함하는 파일 및 히스토그램 이름을 가진 TH2F 히스토그램들을 추출하고 합치는 함수.
    
    :param file_dir: ROOT 파일들이 있는 디렉토리 경로
    :param file_pattern: 파일 이름에 포함된 구문
    :param dir_name: 히스토그램이 저장된 TDirectory 이름
    :param hist_pattern: 히스토그램 이름에 포함된 구문
    :param output_file: 결과를 저장할 ROOT 파일 이름
    """
    merged_hist = None

    # 디렉토리에서 파일 리스트 필터링
    file_list = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if file_pattern in f and f.endswith(".root")]

    for file_path in file_list:
        root_file = ROOT.TFile.Open(file_path)
        if not root_file or root_file.IsZombie():
            print(f"파일 {file_path}을(를) 열 수 없습니다.")
            continue
        
        # TDirectory에서 히스토그램 검색
        directory = root_file.Get(dir_name)
        if not directory:
            print(f"파일 {file_path}에서 디렉토리 {dir_name}을(를) 찾을 수 없습니다.")
            root_file.Close()
            continue

        for key in directory.GetListOfKeys():
            obj_name = key.GetName()
            if hist_pattern in obj_name:  # 히스토그램 이름 필터링
                hist = directory.Get(obj_name)
                if not hist or not isinstance(hist, ROOT.TH2F):
                    print(f"파일 {file_path}에서 {obj_name}이(가) 유효한 TH2F가 아닙니다.")
                    continue
                
                # 히스토그램 병합
                if merged_hist is None:
                    merged_hist = hist.Clone()
                    merged_hist.SetDirectory(0)  # 메모리에 유지
                else:
                    merged_hist.Add(hist)
        
        root_file.Close()

    # 결과를 새 ROOT 파일에 저장
    if merged_hist:
        output_root = ROOT.TFile(output_file, "RECREATE")
        merged_hist.Write()
        output_root.Close()
        print(f"합쳐진 히스토그램이 {output_file}에 저장되었습니다.")
    else:
        print("합쳐질 히스토그램이 없습니다.")

# 예제 실행
file_dir = "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/output_nominal/"  # ROOT 파일들이 있는 디렉토리
file_pattern = "MC"  # 파일 이름에 포함된 구문
dir_name = "plots"  # TDirectory 이름
hist_pattern = "_pt_eta"  # 히스토그램 이름에 포함된 구문
output_file = "merged_histograms.root"  # 저장할 파일 이름

merge_histograms_by_pattern(file_dir, file_pattern, dir_name, hist_pattern, output_file)


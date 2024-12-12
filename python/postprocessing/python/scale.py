import ROOT
import os

# 파일 목록과 각각의 크로스 섹션 값 (fb 단위)
file_info = {
    "hist_DoubleMuon_Data_2018.root": 1,
    "hist_EGamma_Data_2018.root": 1,
    "hist_SingleMuon_Data_2018.root": 1,
    "hist_MuonEG_Data_2018.root": 1,
    "hist_DYJetsToLL_M-10to50_MC_2018.root": 18610,
    "hist_DYJetsToLL_M-50_MC_2018.root": 6077.22,
    "hist_ST_s-channel_MC_2018.root": 3.36,
    "hist_ST_t-channel_antitop_MC_2018.root": 80.95,
    "hist_ST_t-channel_top_MC_2018.root": 136.02,
    "hist_ST_tW_antitop_MC_2018.root": 34.91,
    "hist_ST_tW_top_MC_2018.root": 34.97,
    "hist_TTTo2L2Nu_MC_2018.root": 87.4,
    "hist_TTToHadronic_MC_2018.root": 380,
    "hist_TTToSemiLeptonic_MC_2018.root": 364,
    "hist_WJetsToLNu_MC_2018.root": 61526.7,
    "hist_WW_MC_2018.root": 118.7,
    "hist_WZ_MC_2018.root": 47.13,
    "hist_ZZ_MC_2018.root": 16.523
}

# 루미노시티 값 (fb^-1)
luminosity = 59.6
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

# 각 파일을 처리하는 함수
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

# 모든 파일을 처리하고 새 파일에 저장
for file_name, cross_section in file_info.items():
    histograms = scale_histograms_in_file(file_name, cross_section)
    if histograms is None:
        continue

    # 새 ROOT 파일 작성
    output_file_name = f"scaled_{file_name}"
    output_file = ROOT.TFile.Open(output_file_name, "RECREATE")

    for hist in histograms:
        hist.Write()  # 히스토그램 저장

    output_file.Close()
    print(f"Scaled histograms saved to {output_file_name}")

print("All histograms have been scaled and saved.")

os.system(f"hadd -f Data.root scaled_hist_DoubleMuon_Data_2018.root scaled_hist_EGamma_Data_2018.root scaled_hist_MuonEG_Data_2018.root scaled_hist_SingleMuon_Data_2018.root")
os.system(f"hadd -f TTbar_signal.root scaled_hist_TTTo2L2Nu_MC_2018.root")
os.system(f"hadd -f TTbar_bkg.root scaled_hist_TTToHadronic_MC_2018.root scaled_hist_TTToSemiLeptonic_MC_2018.root")
os.system(f"hadd -f SingleTop.root scaled_hist_ST_*")
os.system(f"hadd -f WZJets.root scaled_hist_DYJets* scaled_hist_WJetsToLNu_MC_2018.root")
os.system(f"hadd -f Diboson.root scaled_hist_WW_MC_2018.root scaled_hist_WZ_MC_2018.root scaled_hist_ZZ_MC_2018.root")
#os.system(f"rm -rf hist_*.root")

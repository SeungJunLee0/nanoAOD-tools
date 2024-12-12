import ROOT
import mplhep as hep
import os

# CMS 스타일 설정
hep.style.use("CMS")

# 파일 및 히스토그램 경로 설정
data_file = "Data.root"
mc_files = {
    "Diboson"         : "Diboson.root",
    "Single top"      : "SingleTop.root",
    "TTbar background": "TTbar_bkg.root",
    "TTbar signal"    : "TTbar_signal.root",
    "W/Z+Jets"        : "WZJets.root"
}
correction_files = {
    "electron_id_down"  : "electron_id_down.root",  
    "electron_id_up"    : "electron_id_up.root",
    "electron_reco_down": "electron_reco_down.root",
    "electron_reco_up"  : "electron_reco_up.root",
    "jet_jer_down"      : "jet_jer_down.root",
    "jet_jer_up"        : "jet_jer_up.root",
    "muon_id_down"      : "muon_id_down.root",
    "muon_id_up"        : "muon_id_up.root",
    "muon_iso_down"     : "muon_iso_down.root",
    "muon_iso_up"       : "muon_iso_up.root",
    "plieup_down"       : "plieup_down.root",
    "plieup_up"         : "plieup_up.root"
}
rebin = 4

def read_and_clone_histogram(file_path, hist_name):
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        print(f"Error: Cannot open file: {file_path}")
        return None
    
    hist = file.Get(hist_name)
    if not hist:
        print(f"Warning: Histogram {hist_name} not found in file {file_path}.")
        file.Close()
        return None
    
    cloned_hist = hist.Clone()  # Clone 메서드를 사용해 복사
    cloned_hist.SetDirectory(0)
    file.Close()
    return cloned_hist

def get_all_histogram_names(file_path):
    """파일에서 모든 히스토그램 이름을 가져오는 함수"""
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        raise RuntimeError(f"Cannot open file: {file_path}")
    hist_names = []
    for key in file.GetListOfKeys():
        obj = key.ReadObj()
        # TH1 계열이면 히스토그램으로 간주
        if isinstance(obj, ROOT.TH1):
            hist_names.append(obj.GetName())
    file.Close()
    return hist_names

# 데이터 파일에서 모든 히스토그램 이름 가져오기
hist_names = get_all_histogram_names(data_file)

# 출력 ROOT 파일 열기 (모든 캔버스를 여기에 기록)
output_root_file = ROOT.TFile("control_plot.root", "RECREATE")

for hist_name in hist_names:
    # 데이터 히스토그램 읽기
    data_hist = read_and_clone_histogram(data_file, hist_name)
    if data_hist is None:
        continue
    data_hist.Rebin(rebin)
    
    # MC 히스토그램 병합
    mc_histograms = {}
    mc_total_hist = None
    for label, file_path in mc_files.items():
        hist = read_and_clone_histogram(file_path, hist_name)
        if hist is None:
            print(f"Skipping {label} for {hist_name} because histogram could not be loaded.")
            continue
        hist.Rebin(rebin)
        mc_histograms[label] = hist
        if mc_total_hist is None:
            mc_total_hist = hist.Clone("mc_total_hist")
        else:
            mc_total_hist.Add(hist)

    # 만약 MC가 하나도 로드 안됐다면 건너뜀
    if mc_total_hist is None:
        print(f"No MC histograms loaded for {hist_name}, skipping.")
        continue
    
    # 캔버스 생성
    canvas = ROOT.TCanvas(f"canvas_{hist_name}", f"Control Plot - {hist_name}", 800, 800)
    canvas.Divide(1, 2)

    # 메인 패드
    main_pad = canvas.cd(1)
    main_pad.SetPad(0, 0.3, 1, 1)
    main_pad.SetBottomMargin(0.02)
    main_pad.SetLogy(False)

    # MC 히스토그램 스택
    stack = ROOT.THStack(f"stack_{hist_name}", "")
    colors = [ROOT.kGreen, ROOT.kOrange, ROOT.kYellow, ROOT.kRed, ROOT.kMagenta]
    for (label, hist), color in zip(mc_histograms.items(), colors):
        hist.SetFillColor(color)
        hist.SetLineColor(ROOT.kBlack)
        stack.Add(hist)

    stack.Draw("HIST")
    stack.GetYaxis().SetTitle("Events")
    stack.GetXaxis().SetLabelSize(0)
    data_hist.SetMarkerStyle(20)
    data_hist.Draw("E SAME")

    # 범례 추가
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(data_hist, "Data", "p")
    for label, hist in mc_histograms.items():
        legend.AddEntry(hist, label, "f")
    legend.Draw()

    # 비율 패드
    ratio_pad = canvas.cd(2)
    ratio_pad.SetPad(0, 0, 1, 0.3)
    ratio_pad.SetTopMargin(0.02)
    ratio_pad.SetBottomMargin(0.3)

    # 비율 계산
    ratio_hist = data_hist.Clone(f"ratio_hist_{hist_name}")
    ratio_hist.Divide(mc_total_hist)
    ratio_hist.SetMarkerStyle(20)
    ratio_hist.GetXaxis().SetTitle(hist_name) # X축 레이블에 hist_name 사용 (원하는 대로 수정 가능)
    ratio_hist.GetYaxis().SetTitle("Data / MC")
    ratio_hist.GetYaxis().SetNdivisions(505)
    ratio_hist.GetYaxis().SetRangeUser(0.4, 1.6)
    ratio_hist.GetYaxis().SetTitleSize(0.1)
    ratio_hist.GetYaxis().SetTitleOffset(0.5)
    ratio_hist.GetYaxis().SetLabelSize(0.08)
    ratio_hist.GetXaxis().SetTitleSize(0.1)
    ratio_hist.GetXaxis().SetLabelSize(0.08)
    ratio_hist.Draw("E")

    # CMS 스타일 레이블
    hep.cms.label("Private Work", data=True, lumi=59.8, loc=0)

    canvas.Draw()
    # 캔버스를 ROOT 파일에 저장
    output_root_file.cd()
    canvas.Write()

output_root_file.Close()


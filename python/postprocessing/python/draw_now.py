import ROOT
import mplhep as hep
import os
from collections import defaultdict

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
    
    # Ratio 히스토그램 계산 (Data/MC)
    ratio_hist = data_hist.Clone(f"ratio_hist_{hist_name}")
    ratio_hist.Divide(mc_total_hist)

    # 여기서 correction_files를 이용해 up/down 불확실성을 계산하는 로직 추가
    # correction_files 안의 히스토그램도 모두 이 히스토그램과 같은 hist_name을 갖는다고 가정
    # systematics_by_type: { "electron_id": {"up": hist_up, "down": hist_down}, ... }
    systematics_by_type = defaultdict(dict)
    for corr_key, corr_file in correction_files.items():
        parts = corr_key.split('_')
        sys_type = '_'.join(parts[:-1]) # ex: "electron_id"
        sys_dir = parts[-1]             # "up" 혹은 "down"

        corr_hist = read_and_clone_histogram(corr_file, hist_name)
        if corr_hist:
            corr_hist.Rebin(rebin)
            # corr_hist는 이 systematic 적용 시의 MC 총합 히스토그램이어야 한다고 가정
            # 만약 correction_files가 이미 합쳐진 MC 히스토그램을 제공한다면 이대로 사용 가능
            # 아니라면 별도의 합산 작업이 필요
            systematics_by_type[sys_type][sys_dir] = corr_hist

    # 시스템 불확실성 합 계산
    # bin 별로 (up - down)/2 를 이용하여 불확실성 추산, Nominal MC 대비 상대 에러 반영
    systematic_unc_sq = [0.0]*(ratio_hist.GetNbinsX()+1)
    for sys_type, variants in systematics_by_type.items():
        if "up" in variants and "down" in variants:
            up_hist = variants["up"]
            down_hist = variants["down"]
            for bin_idx in range(1, ratio_hist.GetNbinsX()+1):
                nominal_mc = mc_total_hist.GetBinContent(bin_idx)
                if nominal_mc == 0:
                    continue
                up_val = up_hist.GetBinContent(bin_idx)
                down_val = down_hist.GetBinContent(bin_idx)
                sys_diff = abs(up_val - down_val) / 2.0
                rel_unc = sys_diff / nominal_mc
                systematic_unc_sq[bin_idx] += rel_unc**2

    # 시스템 불확실성 + 통계 불확실성 결합
    for bin_idx in range(1, ratio_hist.GetNbinsX()+1):
        stat_err = ratio_hist.GetBinError(bin_idx)
        sys_err = (systematic_unc_sq[bin_idx]**0.5)
        total_err = (stat_err**2 + sys_err**2)**0.5
        ratio_hist.SetBinError(bin_idx, total_err)

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

    ratio_hist.SetMarkerStyle(20)
    ratio_hist.GetXaxis().SetTitle(hist_name)
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
print("All histograms processed and saved to control_plot.root.")


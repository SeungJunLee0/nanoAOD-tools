#!/usr/bin/env python3
import ROOT
import mplhep as hep
import os
from collections import defaultdict

# 배치 모드
ROOT.gROOT.SetBatch(True)

# CMS 스타일
hep.style.use("CMS")

# 파일 설정
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

rebin = 2

def read_and_clone_histogram(file_path, hist_name):
    f = ROOT.TFile.Open(file_path)
    if not f or f.IsZombie():
        print(f"Error: Cannot open file: {file_path}")
        return None
    hist = f.Get(hist_name)
    if not hist:
        print(f"Warning: Histogram {hist_name} not found in file {file_path}.")
        f.Close()
        return None
    cloned = hist.Clone()
    cloned.SetDirectory(0)
    f.Close()
    return cloned

def get_all_histogram_names(file_path):
    f = ROOT.TFile.Open(file_path)
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open file: {file_path}")
    hist_names = []
    for key in f.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TH1):
            hist_names.append(obj.GetName())
    f.Close()
    return hist_names

hist_names = get_all_histogram_names(data_file)
output_root_file = ROOT.TFile("control_plot.root", "RECREATE")

for hist_name in hist_names:
    data_hist = read_and_clone_histogram(data_file, hist_name)
    if data_hist is None:
        continue
    data_hist.Rebin(rebin)

    # MC 합치기
    mc_histograms = {}
    mc_total_hist = None
    for label, file_path in mc_files.items():
        mc_hist = read_and_clone_histogram(file_path, hist_name)
        if mc_hist is None:
            continue
        mc_hist.Rebin(rebin)
        mc_histograms[label] = mc_hist
        if mc_total_hist is None:
            mc_total_hist = mc_hist.Clone("mc_total_hist")
        else:
            mc_total_hist.Add(mc_hist)

    if mc_total_hist is None:
        print(f"No MC histograms for {hist_name}, skipping.")
        continue

    # Ratio (Data/MC)
    ratio_hist = data_hist.Clone(f"ratio_hist_{hist_name}")
    ratio_hist.Divide(mc_total_hist)

    # 시스템 불확실성 계산
    systematics_by_type = defaultdict(dict)
    for corr_key, corr_file in correction_files.items():
        parts = corr_key.split('_')
        sys_type = '_'.join(parts[:-1])
        sys_dir = parts[-1]
        corr_hist = read_and_clone_histogram(corr_file, hist_name)
        if corr_hist:
            corr_hist.Rebin(rebin)
            systematics_by_type[sys_type][sys_dir] = corr_hist

    # 상대 시스템 불확실성 제곱합
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
                up_diff = abs(up_val - nominal_mc)
                down_diff = abs(down_val - nominal_mc)
                sys_diff = max(up_diff, down_diff)
                rel_unc = sys_diff / nominal_mc
                systematic_unc_sq[bin_idx] += rel_unc**2

    # --- 메인 패드용 MC 불확실성 밴드 생성 ---
    # 절대 불확실성: sqrt( (stat_err)^2 + (nominal_mc^2)*systematic_unc_sq )
    mc_band_main = ROOT.TGraphAsymmErrors(mc_total_hist.GetNbinsX())
    mc_band_main.SetMarkerStyle(20)
    mc_band_main.SetMarkerSize(1.3)
    mc_band_main.SetLineColor(4)
    mc_band_main.SetFillColor(4)
    mc_band_main.SetFillStyle(3001)

    for bin_idx in range(1, mc_total_hist.GetNbinsX()+1):
        x = mc_total_hist.GetXaxis().GetBinCenter(bin_idx)
        ex = mc_total_hist.GetXaxis().GetBinWidth(bin_idx)*0.5
        nominal_mc = mc_total_hist.GetBinContent(bin_idx)
        mc_stat_err = mc_total_hist.GetBinError(bin_idx)

        # 상대 시스템 불확실성
        sys_rel = (systematic_unc_sq[bin_idx]**0.5)
        # 절대 시스템 불확실성
        sys_abs = sys_rel * nominal_mc

        total_err = (mc_stat_err**2 + sys_abs**2)**0.5

        mc_band_main.SetPoint(bin_idx-1, x, nominal_mc)
        mc_band_main.SetPointError(bin_idx-1, ex, ex, total_err, total_err)

    # --- Ratio 패드용 MC 불확실성 밴드 ---
    mc_band_ratio = ROOT.TGraphAsymmErrors(ratio_hist.GetNbinsX())
    mc_band_ratio.SetMarkerStyle(20)
    mc_band_ratio.SetMarkerSize(1.3)
    mc_band_ratio.SetLineColor(4)
    mc_band_ratio.SetFillColor(4)
    mc_band_ratio.SetFillStyle(3001)

    for bin_idx in range(1, ratio_hist.GetNbinsX()+1):
        x = ratio_hist.GetXaxis().GetBinCenter(bin_idx)
        ex = ratio_hist.GetXaxis().GetBinWidth(bin_idx)*0.5
        nominal_mc = mc_total_hist.GetBinContent(bin_idx)
        if nominal_mc == 0:
            mc_band_ratio.SetPoint(bin_idx-1, x, 1.0)
            mc_band_ratio.SetPointError(bin_idx-1, ex, ex, 0, 0)
            continue

        mc_stat_err = mc_total_hist.GetBinError(bin_idx)
        mc_stat_rel = mc_stat_err/nominal_mc
        sys_rel = (systematic_unc_sq[bin_idx]**0.5)
        total_mc_rel = (mc_stat_rel**2 + sys_rel**2)**0.5

        y = 1.0
        ey = total_mc_rel
        mc_band_ratio.SetPoint(bin_idx-1, x, y)
        mc_band_ratio.SetPointError(bin_idx-1, ex, ex, ey, ey)

    # 캔버스
    canvas = ROOT.TCanvas(f"canvas_{hist_name}", f"Control Plot - {hist_name}", 800, 800)
    canvas.Divide(1, 2)

    # 메인 패드
    main_pad = canvas.cd(1)
    main_pad.SetPad(0, 0.3, 1, 1)
    main_pad.SetBottomMargin(0.02)
    main_pad.SetLogy(False)

    stack = ROOT.THStack(f"stack_{hist_name}", "")
    colors = [ROOT.kGreen, ROOT.kOrange, ROOT.kYellow, ROOT.kRed, ROOT.kMagenta]
    for (label, h), c in zip(mc_histograms.items(), colors):
        h.SetFillColor(c)
        h.SetLineColor(ROOT.kBlack)
        stack.Add(h)

    stack.Draw("HIST")
    stack.GetYaxis().SetTitle("Events")
    stack.GetXaxis().SetLabelSize(0)

    # MC 밴드를 main pad에 추가(E2)
    mc_band_main.Draw("E2 SAME")

    data_hist.SetMarkerStyle(20)
    data_hist.Draw("E SAME")

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(data_hist, "Data", "p")
    for label, h in mc_histograms.items():
        legend.AddEntry(h, label, "f")
    legend.AddEntry(mc_band_main, "MC Unc.", "f")
    legend.Draw()

    # 하단 비율 패드
    ratio_pad = canvas.cd(2)
    ratio_pad.SetPad(0, 0, 1, 0.3)
    ratio_pad.SetTopMargin(0.02)
    ratio_pad.SetBottomMargin(0.3)
    ratio_pad.SetGridy()

    ratio_hist.GetXaxis().SetTitle(hist_name)
    ratio_hist.GetYaxis().SetTitle("Data / MC")
    ratio_hist.GetYaxis().SetNdivisions(505)
    ratio_hist.GetYaxis().SetRangeUser(0, 2)
    ratio_hist.GetYaxis().SetTitleSize(0.1)
    ratio_hist.GetYaxis().SetTitleOffset(0.5)
    ratio_hist.GetYaxis().SetLabelSize(0.08)
    ratio_hist.GetXaxis().SetTitleSize(0.1)
    ratio_hist.GetXaxis().SetLabelSize(0.08)
    ratio_hist.Draw("E")

    # Ratio 패드에 MC 불확실성 밴드
    mc_band_ratio.Draw("E2 SAME")

    hep.cms.label("Private Work", data=True, lumi=59.8, loc=0)

    canvas.Update()
    output_root_file.cd()
    canvas.Write()

output_root_file.Close()
print("All histograms processed and saved to control_plot.root.")


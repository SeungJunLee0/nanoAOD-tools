import ROOT
import mplhep as hep

hep.style.use("CMS")

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

luminosity = 59.6
hist_path = "plots/ee_Twotag_lep1pt"

output_file = ROOT.TFile("output_histograms.root", "RECREATE")
def get_total_entries(file_path):
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        raise RuntimeError(f"Error: Cannot open file: {file_path}")
    hist = file.Get("plots/count")
    if not hist or not isinstance(hist, ROOT.TH1):
        raise RuntimeError(f"Error: 'plots/count' histogram not found or is not a TH1 in file: {file_path}")
    total_entries = hist.Integral()
    #total_entries = hist.GetEntries()
    file.Close()
    return total_entries

def scale_histograms_in_file(file_path, cross_section):
    file = ROOT.TFile.Open(file_path)
    if not file or file.IsZombie():
        print(f"Error: Cannot open file: {file_path}")
        return None

    scale_factor = luminosity * 1000 * cross_section if cross_section >= 2 else 1
    hist = file.Get(hist_path)
    if not hist or not isinstance(hist, ROOT.TH1):
        print(f"Error: Histogram {hist_path} not found in file {file_path}")
        file.Close()
        return None

    if cross_section >= 2:
        hist.Sumw2()  # 오류 계산 활성화
        print(f"Scaled Histogram {hist_path} in {file_path} - Integral: {hist.Integral()}")
        hist.Scale(scale_factor / get_total_entries(file_path))
        print( scale_factor/get_total_entries(file_path))
        print(f"Scaled Histogram {hist_path} in {file_path} - Integral: {hist.Integral()}")
    
    hist.SetDirectory(0)  # 메모리에 유지
    file.Close()
    return hist

data_hist = None
mc_histograms = {}
mc_total_hist = None
colors = [ROOT.kGreen, ROOT.kOrange, ROOT.kYellow, ROOT.kRed, ROOT.kMagenta]

for file_name, cross_section in file_info.items():
    hist = scale_histograms_in_file(file_name, cross_section)
    if hist is None:
        continue

    if cross_section == 1:  
        if data_hist is None:
            data_hist = hist
            data_hist.SetDirectory(0)
        else:
            data_hist.Add(hist)
            data_hist.SetDirectory(0)
    else:
        hist.SetDirectory(0)
        label = file_name.split(".root")[0]
        mc_histograms[label] = hist
        if mc_total_hist is None:
            mc_total_hist = hist.Clone("mc_total_hist")
            mc_total_hist.SetDirectory(0)
        else:
            mc_total_hist.Add(hist)
            mc_total_hist.SetDirectory(0)

if data_hist:
    print(f"Data histogram - Integral: {data_hist.Integral()}")
if mc_total_hist:
    print(f"MC total histogram - Integral: {mc_total_hist.Integral()}")

# 캔버스 생성 및 히스토그램 그리기 (이전 코드와 동일)
canvas = ROOT.TCanvas("canvas", "Control Plot", 800, 800)
canvas.Divide(1, 2)

# 메인 패드 설정
main_pad = canvas.cd(1)
main_pad.SetPad(0, 0.3, 1, 1)
main_pad.SetBottomMargin(0.02)
main_pad.SetLogy(False)

# MC 히스토그램 스택 생성 및 그리기
stack = ROOT.THStack("stack", "")
for (label, hist), color in zip(mc_histograms.items(), colors):
    hist.SetFillColor(color)
    hist.SetLineColor(ROOT.kBlack)
    stack.Add(hist)

stack.Draw("HIST")
stack.GetYaxis().SetTitle("Events / 20 GeV")
stack.GetXaxis().SetLabelSize(0)
data_hist.SetMarkerStyle(20)
data_hist.Draw("E SAME")

# 범례 추가
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(data_hist, "Data", "p")
for label, hist in mc_histograms.items():
    legend.AddEntry(hist, label, "f")
legend.Draw()

# Data/MC 비율 패드 설정
ratio_pad = canvas.cd(2)
ratio_pad.SetPad(0, 0, 1, 0.3)
ratio_pad.SetTopMargin(0.02)
ratio_pad.SetBottomMargin(0.3)

# Data/MC 비율 계산 및 그리기
ratio_hist = data_hist.Clone("ratio_hist")
ratio_hist.Divide(mc_total_hist)
ratio_hist.SetMarkerStyle(20)
ratio_hist.GetXaxis().SetTitle("p_{T}^{t} [GeV]")
ratio_hist.GetYaxis().SetTitle("Data / MC")
ratio_hist.GetYaxis().SetNdivisions(505)
ratio_hist.GetYaxis().SetRangeUser(0.4, 1.6)
ratio_hist.GetYaxis().SetTitleSize(0.1)
ratio_hist.GetYaxis().SetTitleOffset(0.5)
ratio_hist.GetYaxis().SetLabelSize(0.08)
ratio_hist.GetXaxis().SetTitleSize(0.1)
ratio_hist.GetXaxis().SetLabelSize(0.08)
ratio_hist.Draw("E")

# CMS 스타일 레이블 추가
hep.cms.label("Private Work", data=True, lumi=59.8, loc=0)
# 캔버스 출력 및 저장
canvas.Draw()
output_file.Close()
canvas.SaveAs("control_plot.pdf")


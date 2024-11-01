import ROOT
import mplhep as hep

# CMS 스타일 설정
hep.style.use("CMS")

# 파일 및 히스토그램 경로 설정
data_file = "Data.root"
mc_files = {
#    "Diboson"         : "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/Diboson.root",
#    "Single top"      : "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/SingleTop.root",
#    "TTbar background": "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/TTbar_bkg.root",
#    "TTbar signal"    : "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/TTbar_signal.root",
#    "W/Z+Jets"        : "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python/WZJets.root"
    "Diboson"         : "Diboson.root",
    "Single top"      : "SingleTop.root",
    "TTbar background": "TTbar_bkg.root",
    "TTbar signal"    : "TTbar_signal.root",
    "W/Z+Jets"        : "WZJets.root"
}
hist_path = "ee_Twotag_lep1pt"

# 히스토그램 읽기 및 Clone
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
    print(cloned_hist)
    return cloned_hist

# 데이터 히스토그램 읽기
data_hist = read_and_clone_histogram(data_file, hist_path)
if data_hist is None:
    raise RuntimeError("Data histogram could not be loaded. Check the file path and histogram name.")

# MC 히스토그램 병합
mc_histograms = {}
mc_total_hist = None
for label, file_path in mc_files.items():
    hist = read_and_clone_histogram(file_path, hist_path)
    if hist is None:
        print(f"Skipping {label} because histogram could not be loaded.")
        continue  # 히스토그램이 없으면 건너뛰기
    mc_histograms[label] = hist
    if mc_total_hist is None:
        mc_total_hist = hist.Clone("mc_total_hist")
    else:
        mc_total_hist.Add(hist)

# 오류 처리: MC 히스토그램 병합본이 None일 경우
if mc_total_hist is None:
    raise RuntimeError("MC histograms could not be loaded. Check the file paths and histogram names.")

# 캔버스 생성
canvas = ROOT.TCanvas("canvas", "Control Plot", 800, 800)
canvas.Divide(1, 2)

# 메인 패드 설정
main_pad = canvas.cd(1)
main_pad.SetPad(0, 0.3, 1, 1)
main_pad.SetBottomMargin(0.02)
main_pad.SetLogy(False)

# MC 히스토그램 그리기
stack = ROOT.THStack("stack", "")
colors = [ROOT.kGreen, ROOT.kOrange, ROOT.kYellow, ROOT.kRed, ROOT.kMagenta]
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

# 캔버스 출력
canvas.Draw()
canvas.SaveAs("control_plot.png")


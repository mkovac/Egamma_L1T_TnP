import ROOT
import TurnOnPlot_DATA as TurnOnPlot
from ROOT import RooCurve, RooHist, RooAbsData


plots = []
plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_prompt_plot"
plots[-1].xRange = (5,1000)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)

plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_diff_prompt_plot"
plots[-1].xRange = (5,1000)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.45,0.2,0.9,0.3)

plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_diff_prompt-new_plot"
plots[-1].xRange = (5,1000)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.45,0.2,0.9,0.3)

inputFile = ROOT.TFile.Open("./TestTurnOn/fitOutput.root")

	
histo = inputFile.Get("histo_Stage2_vs_Pt_35GeV_1")
histo.__class__ = ROOT.RooHist
	
fit   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_1")
fit.__class__ = ROOT.RooCurve

turnon = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo, Fit=fit,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=21, LineColor=ROOT.kBlack,LineStyle=1,
                                    Legend="Data")

histo2 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_2")
histo2.__class__ = ROOT.RooHist
	
fit2   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_2")
fit2.__class__ = ROOT.RooCurve

turnon2 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo2, 
                                    MarkerColor=ROOT.kRed, MarkerStyle=20, LineColor=ROOT.kRed,LineStyle=1,
                                    Legend="New pedestals")

histo3 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_3")
histo3.__class__ = ROOT.RooHist
	
fit3   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_3")
fit3.__class__ = ROOT.RooCurve

turnon3 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo3, 
                                    MarkerColor=ROOT.kBlue, MarkerStyle=22, LineColor=ROOT.kRed,LineStyle=1,
                                    Legend="Prompt pedestals")
plots[0].addTurnOn(turnon)
plots[0].addTurnOn(turnon2)
plots[0].addTurnOn(turnon3)

#Plot the difference:
diffcurve=RooCurve("diff","diff",fit, fit3, 1,-1)
diffhist=RooHist(histo,histo3,1,-1,RooAbsData.SumW2)
turnondiff = TurnOnPlot.TurnOn(Name="Stage2", Histo=diffhist, Fit=diffcurve,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=20, LineColor=ROOT.kBlue,LineStyle=1,
                                    Legend="Data-Prompt_pedestals")

plots[1].addTurnOn(turnondiff)

newdiffcurve=RooCurve("newdiff","newdiff",fit2, fit3, 1,-1)
newdiffhist=RooHist(histo2,histo3,1,-1,RooAbsData.SumW2)
newturnondiff = TurnOnPlot.TurnOn(Name="Stage2", Histo=newdiffhist, Fit=newdiffcurve,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=20, LineColor=ROOT.kBlue,LineStyle=1,
                                    Legend="New_pedestals-Prompt_pedestals")

plots[2].addTurnOn(newturnondiff)


canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()


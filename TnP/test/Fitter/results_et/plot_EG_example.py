import ROOT
import TurnOnPlot_DATA as TurnOnPlot
from ROOT import RooCurve, RooHist, RooAbsData


plots = []
plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_plot"
plots[-1].xRange = (5,1000)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)

plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_diff_plot"
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

plots[0].addTurnOn(turnon)
plots[0].addTurnOn(turnon2)

#Plot the difference:
diffcurve=RooCurve("diff","diff",fit, fit2, 1,-1)
diffhist=RooHist(histo,histo2,1,-1,RooAbsData.SumW2)
turnondiff = TurnOnPlot.TurnOn(Name="Stage2", Histo=diffhist, Fit=diffcurve,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=20, LineColor=ROOT.kBlue,LineStyle=1,
                                    Legend="Data-New_pedestals")

plots[1].addTurnOn(turnondiff)



canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()


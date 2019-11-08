import ROOT
import TurnOnPlot_DATA as TurnOnPlot
from ROOT import RooCurve, RooHist, RooAbsData


plots = []
plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_plot"
plots[-1].xRange = (5,1000)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)

inputFile = ROOT.TFile.Open("./TestTurnOn/fitOutput.root")

	
histo = inputFile.Get("histo_Stage2_vs_Pt_35GeV_1")
histo.__class__ = ROOT.RooHist
	
fit   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_1")
fit.__class__ = ROOT.RooCurve

turnon = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo, Fit=fit,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=21, LineColor=ROOT.kBlack,LineStyle=1,
                                    Legend="Data")

plots[0].addTurnOn(turnon)




canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()


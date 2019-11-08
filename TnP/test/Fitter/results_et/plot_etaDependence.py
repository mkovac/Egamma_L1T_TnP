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

	
histo1 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_1")
histo1.__class__ = ROOT.RooHist
	
fit1   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_1")
fit1.__class__ = ROOT.RooCurve

turnon1 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo1, Fit=fit1,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack,LineStyle=1,
                                    Legend="0<Eta<0.5")


histo2 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_2")
histo2.__class__ = ROOT.RooHist
	
fit2   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_2")
fit2.__class__ = ROOT.RooCurve

turnon2 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo2, Fit=fit2,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+1,LineStyle=2,
                                    Legend="0.5<Eta<1")


histo3 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_3")
histo3.__class__ = ROOT.RooHist
	
fit3   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_3")
fit3.__class__ = ROOT.RooCurve

turnon3 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo3, Fit=fit3,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+2,LineStyle=3,
                                    Legend="1<Eta<1.5")

histo4 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_4")
histo4.__class__ = ROOT.RooHist
	
fit4   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_4")
fit4.__class__ = ROOT.RooCurve

turnon4 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo4, Fit=fit4,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+3,LineStyle=4,
                                    Legend="1.5<Eta<2")



histo5 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_5")
histo5.__class__ = ROOT.RooHist
	
fit5   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_5")
fit5.__class__ = ROOT.RooCurve

turnon5 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo5, Fit=fit5,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+4,LineStyle=5,
                                    Legend="2<Eta<2.5")



histo6 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_6")
histo6.__class__ = ROOT.RooHist
	
fit6   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_6")
fit6.__class__ = ROOT.RooCurve

turnon6 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo6, Fit=fit6,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+5,LineStyle=6,
                                    Legend="2.5<Eta<3")

histo7 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_7")
histo7.__class__ = ROOT.RooHist
	
fit7   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_7")
fit7.__class__ = ROOT.RooCurve

turnon7 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo7, Fit=fit7,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+6,LineStyle=7,
                                    Legend="3<Eta<3.5")

histo8 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_8")
histo8.__class__ = ROOT.RooHist
	
fit8   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_8")
fit8.__class__ = ROOT.RooCurve

turnon8 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo8, Fit=fit8,
                                    LineColor=ROOT.kBlack, MarkerStyle=21, MarkerColor=ROOT.kBlack+8,LineStyle=8,
                                    Legend="3.5<Eta<4")

#plots[0].addTurnOn(turnon1)
#plots[0].addTurnOn(turnon2)
#plots[0].addTurnOn(turnon3)
#plots[0].addTurnOn(turnon4)
#plots[0].addTurnOn(turnon5)
plots[0].addTurnOn(turnon6)
plots[0].addTurnOn(turnon7)
plots[0].addTurnOn(turnon8)




canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()


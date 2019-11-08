import FWCore.ParameterSet.Config as cms


HLTLISTTAG = cms.VPSet(
    cms.PSet (
        HLT = cms.string("HLT_Ele27_WPTight_Gsf_v"),
        path1 = cms.vstring ("hltEle27WPTightGsfTrackIsoFilter"), #FIXME: to check
        path2 = cms.vstring (""),
        leg1 = cms.int32(11),
        leg2 = cms.int32(999)
        ),
)

HLTLISTPROBE = cms.VPSet(
    cms.PSet (
        HLT = cms.string("HLT_Ele27_WPTight_Gsf_v"),
        path1 = cms.vstring ("hltEle27WPTightGsfTrackIsoFilter"), #FIXME: to check
        path2 = cms.vstring (""),
        leg1 = cms.int32(11),
        leg2 = cms.int32(999)
        ),
)



# filter HLT paths for T&P
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
hltFilter = hlt.hltHighLevel.clone(
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    #TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    #TriggerResultsTag = cms.InputTag("TriggerResults","","RECO"),
    #TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    #TriggerResultsTag = cms.InputTag("TriggerResults","","HLT2"),
    HLTPaths = ['HLT_Ele27_WPTight_Gsf_v'],
    andOr = cms.bool(True), # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
    throw = cms.bool(True) #if True: throws exception if a trigger path is invalid
)



Ntuplizer = cms.EDAnalyzer("Ntuplizer",
    treeName = cms.string("TagAndProbe"),
    electrons = cms.InputTag("gedGsfElectrons"),
    genParticles = cms.InputTag("genParticles"),                       
    eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90"),
    eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-HZZ-V1-wpLoose"),                           
    triggerSet = cms.InputTag("selectedPatTrigger"),
    #triggerResultsLabel = cms.InputTag("TriggerResults", "", "HLT"),
    #triggerResultsLabel = cms.InputTag("TriggerResults", "", "HLT"),
    triggerResultsLabel = cms.InputTag("TriggerResults", "", "RECO"),
    #triggerResultsLabel = cms.InputTag("TriggerResults", "", "HLT2"),
    #triggerResultsLabel = cms.InputTag("TriggerResults", "", "HLT"),    
    L1EG = cms.InputTag("caloStage2Digis", "EGamma", "RECO"),
    L1EmuEG = cms.InputTag("simCaloStage2Digis", "MP"),
    Vertices = cms.InputTag("offlinePrimaryVertices"),
    triggerListTag = HLTLISTTAG,
    triggerListProbe = HLTLISTPROBE,
    useGenMatch = cms.bool(True),
    useHLTMatch = cms.bool(True)
)



NtupleSeq = cms.Sequence(
    #hltFilter      +
    Ntuplizer
)

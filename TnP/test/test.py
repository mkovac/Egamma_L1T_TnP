import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms

process = cms.Process("TagAndProbe")

isMC = False
isMINIAOD = True

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")


options = VarParsing.VarParsing ('analysis')

options.register ('skipEvents',
                  -1, # default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "Number of events to skip")
                  
options.register ('JSONfile',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "JSON file (empty for no JSON)")
                  
options.outputFile = 'TnP_test.root'
options.inputFiles = []
options.maxEvents  = 200
options.parseArguments()


###############
# Electron ID #
###############

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")

dataFormat = DataFormat.AOD
if isMINIAOD:
   dataFormat = DataFormat.MiniAOD
    
switchOnVIDElectronIdProducer(process, dataFormat)

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")

# Overwrite a default parameter: for miniAOD, the collection name is a slimmed one
if isMINIAOD:
   process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')

from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Define which IDs we want to produce. Each of these two example IDs contains all four standard.
my_id_modules = [
#   'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',      # Both 25 and 50 ns cutbased ids produced
#   'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
#   'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                   # Recommended for both 50 and 25 ns
#   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff',   # Will not be produced for 50 ns, triggering still to come
#   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',      # 25 ns trig
#   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',      # 50 ns trig
#   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff', # Spring16
#   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',            # Spring16 HZZ
   'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff', 
                ] 


# Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)


egmMod = 'egmGsfElectronIDs'
mvaMod = 'electronMVAValueMapProducer'
regMod = 'electronRegressionValueMapProducer'
egmSeq = 'egmGsfElectronIDSequence'

setattr(process, egmMod, process.egmGsfElectronIDs.clone())
setattr(process, mvaMod, process.electronMVAValueMapProducer.clone())
setattr(process, regMod, process.electronRegressionValueMapProducer.clone())

setattr(process, egmSeq, cms.Sequence(getattr(process, mvaMod)*getattr(process, egmMod)*getattr(process, regMod)))
process.electrons = cms.Sequence(getattr(process, mvaMod)*getattr(process, egmMod)*getattr(process, regMod))


if not isMC:
   from Configuration.AlCa.autoCond import autoCond
   process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v9'
   process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
   process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring('/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v1/000/319/349/00000/F0D65BC0-DF84-E811-B9D4-FA163E92EB41.root'),
)
else:
   process.GlobalTag.globaltag = '94X_mcRun2_asymptotic_v0'
   process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
   process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring(            
#                  '/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/120000/02A210D6-F5C3-E611-B570-008CFA197BD4.root'      
                  '/store/mc/RunIISummer16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RAWAODSIM/FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/110000/005BFB99-EBA9-E611-8850-0CC47A4D762A.root')
)

   process.Ntuplizer.useHLTMatch = cms.bool(False) # In case no HLT object in MC sample considered or you're fed up with trying to find the right HLT collections.


if isMINIAOD:
   process.Ntuplizer.electrons = cms.InputTag("slimmedElectrons")
   process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
   process.Ntuplizer.Vertices = cms.InputTag("offlineSlimmedPrimaryVertices")

if options.JSONfile:
   print "Using JSON: " , options.JSONfile
   process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
   process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(-1)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)


process.p = cms.Path(
    process.electrons +
    process.NtupleSeq
)

#process.schedule = cms.Schedule(process.p)


# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
#from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAW

#call to customisation function L1NtupleRAWEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
#process = L1NtupleRAW(process)


# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService', fileName = cms.string(options.outputFile))

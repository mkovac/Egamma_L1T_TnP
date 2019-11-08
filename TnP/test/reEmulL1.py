import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("TagAndProbe", eras.Run2_2018)

isMC = False
isMINIAOD = True

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


#options.register ('secondaryFilesList','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "List of secondary input files")
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
        
options.outputFile = 'NTuple.root'
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

setattr(process,egmMod,process.egmGsfElectronIDs.clone())
setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
setattr(process,regMod,process.electronRegressionValueMapProducer.clone())

setattr(process,egmSeq,cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod)))
process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod))

#process.load('EGTagAndProbe.EGTagAndProbe.triggerProducer_cfi')

import FWCore.Utilities.FileUtils as FileUtils
#listSecondaryFiles = FileUtils.loadListFromFile (options.secondaryFilesList)

if not isMC:
   from Configuration.AlCa.autoCond import autoCond
   process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v9'

   process.GlobalTag.toGet = cms.VPSet(
      cms.PSet(record = cms.string("EcalTPGLinearizationConstRcd"),
               tag = cms.string("EcalTPGLinearizationConst_IOV_319253_beginning_at_1"),
               connect = cms.string('sqlite_file:EcalTPG_trans_319253_pedes_319111_moved_to_1.db')),
      cms.PSet(record = cms.string("EcalTPGPedestalsRcd"),
               tag = cms.string("EcalTPGPedestals_319253_beginning_at_1"),
	            connect =cms.string('sqlite_file:EcalTPG_trans_319253_pedes_319111_moved_to_1.db')))

   process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
   
   process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring('/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v1/000/319/349/00000/F0D65BC0-DF84-E811-B9D4-FA163E92EB41.root'),

      secondaryFileNames = cms.untracked.vstring(
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/F2B54F09-EC82-E811-B4AE-FA163EADDAA1.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/EC79DFD9-F082-E811-88C0-02163E010DA6.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/EC5958BD-4583-E811-A824-FA163E0F5CB9.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/DA94DCAB-4583-E811-A797-FA163E86050D.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/D4EDCFA6-4583-E811-AFD4-FA163E6AFA09.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/D4E48DA6-4583-E811-8A69-FA163E7293B4.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/C010A19E-4583-E811-B543-FA163E741AF7.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/AE0E13EB-F082-E811-B346-02163E01A01A.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/AA05BE93-4583-E811-8AD2-FA163E70B547.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/A607CF93-4583-E811-9599-FA163E2322D8.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/8254E883-F082-E811-9A7C-FA163E920180.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/7C00D48D-4583-E811-A1CB-FA163ECD65AF.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/68C66586-4583-E811-BDFE-FA163EBC9859.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/2021C1EF-4583-E811-9330-FA163EEBE817.root',
         '/store/data/Run2018C/EGamma/RAW/v1/000/319/347/00000/1E500EA3-4583-E811-A90B-FA163E0BD5CE.root'
      )
   )

#   process.source.eventsToProcess = cms.untracked.VEventRange('281613:108:12854629')


if isMINIAOD:
   process.Ntuplizer.electrons = cms.InputTag("slimmedElectrons")
   process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
   process.Ntuplizer.Vertices = cms.InputTag("offlineSlimmedPrimaryVertices")
#   process.Ntuplizer.triggerSet = cms.InputTag("slimmedPatTrigger","","RECO")
else:
#    process.GlobalTag.globaltag = 'auto:run2_mc' #MC 25 ns miniAODv2
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_v14'
#    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
#    process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring(
#      '/store/mc/RunIISpring16DR80/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/40000/AA918EB1-6E64-E611-9BE0-00259074AE54.root'
      '/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/1A13CB76-9B67-E611-A143-0050560210EC.root'
      ),
#      secondaryFileNames = cms.untracked.vstring(listSecondaryFiles)
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/00000/08D2C535-5458-E511-B0C0-FA163E83549A.root'
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/10000/8A2D3925-4658-E511-80B2-02163E014126.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/10000/ECB7FC03-8058-E511-BE9D-02163E0141A2.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/4473DFF5-9456-E511-9C4B-002590494C8A.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/587A9A92-A956-E511-AC52-0025904B11CC.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7076052C-4A57-E511-B371-00259074AE9A.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7CD6A6C7-9C56-E511-87E5-003048C75840.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7E281C8E-4357-E511-8498-00259074AE80.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/98884797-4957-E511-82C6-00259073E504.root',
#         '/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/BE274E99-4957-E511-88ED-0025907A1A2E.root',
   )

process.schedule = cms.Schedule()


# L1 emulation stuff
if not isMC:
   from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAWsimEcalTP 
   process = L1TReEmulFromRAWsimEcalTP(process)
else:
   from L1Trigger.Configuration.customiseReEmul import L1TReEmulMCFromRAW
   process = L1TReEmulMCFromRAW(process) 
   from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 
   process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)

process.load("L1Trigger.L1TCalorimeter.caloParams_2018_v1_3_cfi")


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

 
process.p = cms.Path (
        process.electrons +
        process.RawToDigi +
        process.L1TReEmul +
        process.NtupleSeq #+
        #process.patTriggerSeq        
        )


'''
## Pantelis
process.p = cms.Path(process.electrons)
print("after process.electrons")
process.p = cms.Path(process.RawToDigi)
print("after process.RawToDigi")
process.p = cms.Path(process.L1TReEmul)
print("after process.L1TReEmul")
process.p = cms.Path(process.NtupleSeq)
print("after process.NtupleSeq")
'''





 


process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))

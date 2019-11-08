# TEMPLATE used for automatic script submission of multiple datasets

from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'TagAndProbe'
config.General.workArea = 'DefaultCrab3Area_ped319111'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'reEmulL1.py'
config.JobType.inputFiles = ['EcalTPG_trans_319253_pedes_319111_moved_to_1.db']
#config.JobType.allowUndistributedCMSSW = True
config.section_("Data")
config.Data.inputDataset = '/EGamma/Run2018C-PromptReco-v1/MINIAOD'  #'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80-FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/RAWAODSIM'

########################################### Parent Dataset #######################################
config.Data.secondaryInputDataset= '/EGamma/Run2018C-v1/RAW'#'/SingleElectron/Run2017F-v1/RAW'
##################################################################################################

config.Data.inputDBS = 'global'
#config.Data.runRange =  '300742-301283'
config.Data.runRange =  '319347'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 15000 #number of events per jobs
config.Data.totalUnits = -999 #number of event
config.Data.outLFNDirBase = '/store/user/syuan/TagAndProbeTrees/Emulation/callibrations/reEmulrunC'  #'/store/user/tstreble/TagAndProbeTrees'
#config.Data.outLFNDirBase = '/eos/user/s/syuan/TagAndProbeTrees/Emulation/callibrations'  #'/store/user/tstreble/TagAndProbeTrees'
config.Data.publication = False
config.Data.outputDatasetTag = 'TagAndProbe_ped319111'
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt'
# json with 3.99/fb

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.storageSite = 'T2_CH_CERN'
#config.Data.ignoreLocality=True
config.Site.blacklist = ['T3_TW_NTU_HEP', 'T3_GR_IASA', 'T2_GR_Ioannina', 'T3_MX_Cinvestav', 'T2_DE_RWTH', 'T2_UK_SGrid_RALPP', 'T3_RU_FIAN', 'T2_FI_HIP', 'T2_BR_SPRACE', 'T2_ES_CIEMAT', 'T2_EE_Estonia', 'T3_US_UCR', 'T3_US_UMiss']


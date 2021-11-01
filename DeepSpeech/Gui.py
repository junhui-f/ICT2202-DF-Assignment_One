# This python autopsy module is an example of the different types of 
# things you can do with the GUI portion of an Autopsy Pythin plugin
#
# Contact: Mark McKinnon [Mark [dot] McKinnon <at> gmail [dot] com]
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# GUI_Test module.
# February 2017
# 
# Comments 
#   Version 1.0 - Initial version - Feb 2017
# 

import jarray
import inspect
import os
from subprocess import Popen, PIPE

from javax.swing import JCheckBox
from javax.swing import JButton
from javax.swing import ButtonGroup
from javax.swing import JComboBox
from javax.swing import JList
from javax.swing import JTextArea
from javax.swing import JTextField
from javax.swing import JLabel
from javax.swing.event import DocumentEvent
from javax.swing.event import DocumentListener
from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
from java.awt import Color
from javax.swing import JPanel
from javax.swing import JScrollPane
from javax.swing import JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter


from java.lang import Class
from java.lang import System
from java.sql  import DriverManager, SQLException
from java.util.logging import Level
from java.io import File
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import GenericIngestModuleJobSettings
from org.sleuthkit.autopsy.ingest import IngestModuleIngestJobSettingsPanel
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.ingest import ModuleDataEvent
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.coreutils import PlatformUtil
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.datamodel import ContentUtils



# Factory that defines the name and details of the module and allows Autopsy
# to create instances of the modules that will do the analysis.
class GUI_TestIngestModuleFactory(IngestModuleFactoryAdapter):

    def __init__(self):
        self.settings = None

    moduleName = "GUI Test"
    
    def getModuleDisplayName(self):
        return self.moduleName
    
    def getModuleDescription(self):
        return "GUI Test Example"
    
    def getModuleVersionNumber(self):
        return "1.0"
    
    def getDefaultIngestJobSettings(self):
        return GenericIngestModuleJobSettings()

    def hasIngestJobSettingsPanel(self):
        return True

    # TODO: Update class names to ones that you create below
    def getIngestJobSettingsPanel(self, settings):
        if not isinstance(settings, GenericIngestModuleJobSettings):
            raise IllegalArgumentException("Expected settings argument to be instanceof GenericIngestModuleJobSettings")
        self.settings = settings
        return GUI_TestWithUISettingsPanel(self.settings)

    def isDataSourceIngestModuleFactory(self):
        return True

    def createDataSourceIngestModule(self, ingestOptions):
        return GUI_TestIngestModule(self.settings)

# Data Source-level ingest module.  One gets created per data source.
class GUI_TestIngestModule(DataSourceIngestModule):

    _logger = Logger.getLogger(GUI_TestIngestModuleFactory.moduleName)

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def __init__(self, settings):
        self.context = None
        self.local_settings = settings
        self.List_Of_GUI_Test = []

    # Where any setup and configuration is done
    # 'context' is an instance of org.sleuthkit.autopsy.ingest.IngestJobContext.
    # See: http://sleuthkit.org/autopsy/docs/api-docs/3.1/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_ingest_job_context.html
    def startUp(self, context):
        self.context = context

        Combo_Box_entry = self.local_settings.getSetting('ComboBox')
        self.log(Level.INFO, "Combo Box Entry Starts here =====>")
        self.log(Level.INFO, self.local_settings.getSetting('ComboBox'))
        self.log(Level.INFO, "<====== Combo Box Entry Ends here")

        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        # raise IngestModuleException(IngestModule(), "Oh No!")
        pass

    # Where the analysis is done.
    # The 'dataSource' object being passed in is of type org.sleuthkit.datamodel.Content.
    # See:x http://www.sleuthkit.org/sleuthkit/docs/jni-docs/interfaceorg_1_1sleuthkit_1_1datamodel_1_1_content.html
    # 'progressBar' is of type org.sleuthkit.autopsy.ingest.DataSourceIngestModuleProgress
    # See: http://sleuthkit.org/autopsy/docs/api-docs/3.1/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_data_source_ingest_module_progress.html
    def process(self, dataSource, progressBar):

        self.log(Level.INFO, "Starting to process, Just before call to parse_safari_history")

        # we don't know how much work there is yet
        progressBar.switchToIndeterminate()
        
        self.log(Level.INFO, "Starting 2 to process, Just before call to ???????")
        self.log(Level.INFO, "ending process, Just before call to ??????")
        
        # After all databases, post a message to the ingest messages in box.
        message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
            "GUI_Test", " GUI_Test Has Been Analyzed " )
        IngestServices.getInstance().postMessage(message)

        return IngestModule.ProcessResult.OK     



# UI that is shown to user for each ingest job so they can configure the job.
# TODO: Rename this
class GUI_TestWithUISettingsPanel(IngestModuleIngestJobSettingsPanel):
    # Note, we can't use a self.settings instance variable.
    # Rather, self.local_settings is used.
    # https://wiki.python.org/jython/UserGuide#javabean-properties
    # Jython Introspector generates a property - 'settings' on the basis
    # of getSettings() defined in this class. Since only getter function
    # is present, it creates a read-only 'settings' property. This auto-
    # generated read-only property overshadows the instance-variable -
    # 'settings'
    
    # We get passed in a previous version of the settings so that we can
    # prepopulate the UI
    # TODO: Update this for your UI
    def __init__(self, settings):
        self.local_settings = settings
        self.initComponents()
        self.customizeComponents()
    
    # Select Model File onClick Event
    def selectModelFile(self, e):

        chooseFile = JFileChooser()
        filter = FileNameExtensionFilter(".pbmm", ["pbmm"])
        chooseFile.setAcceptAllFileFilterUsed(False);
        chooseFile.setFileFilter(filter)

        ret = chooseFile.showDialog(self.panel0, "Select Model File")
        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            Canonical_file = file.getCanonicalPath()
            self.ModelFile_TF.setText(Canonical_file)

    # Select Scorer File onClick Event
    def selectScorerFile(self, e):

        chooseFile = JFileChooser()
        filter = FileNameExtensionFilter(".scorer", ["scorer"])
        chooseFile.setAcceptAllFileFilterUsed(False);
        chooseFile.setFileFilter(filter)

        ret = chooseFile.showDialog(self.panel0, "Select Scorer File")
        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            Canonical_file = file.getCanonicalPath()
            self.ScorerFile_TF.setText(Canonical_file)

    # Modify beam_width field event
    def beam_width_mod(self, e):
        self.ScorerFile_TF.setText("1")

    # Modify lm_alpha field event
    def lm_alpha_mod(self, e):
        self.ScorerFile_TF.setText("2")

    # Modify lm_beta field event
    def lm_beta_mod(self, e):
        self.ScorerFile_TF.setText("3")

    # Check if VAD is enabled
    def checkVAD(self, e):
        if self.vad_CheckBox.isSelected():
            self.VAD_CB.setEnabled(True)
        else:
            self.VAD_CB.setEnabled(False)

    # Modify VAD Verbosity Event
    def modifyVAD(self, e):
        self.ScorerFile_TF.setText("4")

    # TODO: Update this for your UI
    def initComponents(self):
        self.panel0 = JPanel()

        self.rbgPanel0 = ButtonGroup() 
        self.gbPanel0 = GridBagLayout() 
        self.gbcPanel0 = GridBagConstraints() 
        self.panel0.setLayout( self.gbPanel0 ) 

        # First Row: Select Model File
        self.label_ModelFile = JLabel("Model File")
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 1 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.label_ModelFile, self.gbcPanel0 )
        self.panel0.add(self.label_ModelFile)

        self.ModelFile_TF = JTextField(20) 
        self.ModelFile_TF.setEditable(False)
        self.ModelFile_TF.setBackground(Color.WHITE)
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 3 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.ModelFile_TF, self.gbcPanel0 ) 
        self.panel0.add( self.ModelFile_TF ) 

        self.FindModelFile_BTN = JButton( "Browse", actionPerformed=self.selectModelFile) 
        self.rbgPanel0.add( self.FindModelFile_BTN ) 
        self.gbcPanel0.gridx = 6 
        self.gbcPanel0.gridy = 3 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.FindModelFile_BTN, self.gbcPanel0 ) 
        self.panel0.add( self.FindModelFile_BTN ) 

        # Second Row: Select Scorer File
        self.label_ScorerFile = JLabel("Scorer File")
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 5 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.label_ScorerFile, self.gbcPanel0 )
        self.panel0.add(self.label_ScorerFile)

        self.ScorerFile_TF = JTextField(20) 
        self.ScorerFile_TF.setEditable(False)
        self.ScorerFile_TF.setBackground(Color.WHITE)
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 8
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.ScorerFile_TF, self.gbcPanel0 ) 
        self.panel0.add( self.ScorerFile_TF ) 

        self.FindScorerFile_BTN = JButton( "Browse", actionPerformed=self.selectScorerFile) 
        self.rbgPanel0.add( self.FindScorerFile_BTN ) 
        self.gbcPanel0.gridx = 6 
        self.gbcPanel0.gridy = 8 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.FindScorerFile_BTN, self.gbcPanel0 ) 
        self.panel0.add( self.FindScorerFile_BTN ) 

        # Third Row: Manual input beam_width 
        self.label_beam_width = JLabel("Beam_width")
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 10 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.label_beam_width, self.gbcPanel0 )
        self.panel0.add(self.label_beam_width)

        self.beam_width_TF = JTextField("100",20)
        self.beam_width_TF.getDocument().insertUpdate = self.beam_width_mod
        self.beam_width_TF.getDocument().removeUpdate = self.beam_width_mod
        self.beam_width_TF.getDocument().changedUpdate = self.beam_width_mod
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 13
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.beam_width_TF, self.gbcPanel0 ) 
        self.panel0.add( self.beam_width_TF ) 

        # Fourth Row: Manual input lm_alpha 
        self.label_lm_alpha = JLabel("lm_alpha")
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 15 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.label_lm_alpha, self.gbcPanel0 )
        self.panel0.add(self.label_lm_alpha)

        self.lm_alpha_TF = JTextField("100",20)
        self.lm_alpha_TF.getDocument().insertUpdate = self.lm_alpha_mod
        self.lm_alpha_TF.getDocument().removeUpdate = self.lm_alpha_mod
        self.lm_alpha_TF.getDocument().changedUpdate = self.lm_alpha_mod
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 19
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.lm_alpha_TF, self.gbcPanel0 ) 
        self.panel0.add( self.lm_alpha_TF ) 

        # Fifth Row: Manual input lm_beta
        self.label_lm_beta = JLabel("lm_beta")
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 21 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.label_lm_beta, self.gbcPanel0 )
        self.panel0.add(self.label_lm_beta)

        self.lm_beta_TF = JTextField("100",20)
        self.lm_beta_TF.getDocument().insertUpdate = self.lm_beta_mod
        self.lm_beta_TF.getDocument().removeUpdate = self.lm_beta_mod
        self.lm_beta_TF.getDocument().changedUpdate = self.lm_beta_mod
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 25
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.lm_beta_TF, self.gbcPanel0 ) 
        self.panel0.add( self.lm_beta_TF ) 

        # Sixth Row: Enable VAD (T/F) w. Verbosity
        self.vad_CheckBox = JCheckBox( "Enable VAD", actionPerformed=self.checkVAD)
        self.vad_CheckBox.setSelected(True)
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 27 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.vad_CheckBox, self.gbcPanel0 ) 
        self.panel0.add( self.vad_CheckBox ) 

        self.dataVAD_CB = ("Low", "Medium", "High", "Very High")
        self.VAD_CB = JComboBox( self.dataVAD_CB)
        self.VAD_CB.itemStateChanged = self.modifyVAD      
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 31 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.VAD_CB, self.gbcPanel0 ) 
        self.panel0.add( self.VAD_CB ) 

        self.add(self.panel0)

    # TODO: Update this for your UI
    def customizeComponents(self):
        pass

    # Return the settings used
    def getSettings(self):
        return self.local_settings



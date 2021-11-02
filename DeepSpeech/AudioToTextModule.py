# Sample module in the public domain. Feel free to use this as a template
# for your modules (and you can remove this header and take complete credit
# and liability)
#
# Contact: Brian Carrier [carrier <at> sleuthkit [dot] org]
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

# Simple file-level ingest module for Autopsy.
# Search for TODO for the things that you need to change
# See http://sleuthkit.org/autopsy/docs/api-docs/4.6.0/index.html for documentation

import jarray
import inspect
import os
from subprocess import Popen, PIPE

from javax.swing import JCheckBox
from javax.swing import JButton
from javax.swing import ButtonGroup
from javax.swing import JList
from javax.swing import JTextArea
from javax.swing import JTextField
from javax.swing import JLabel
from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
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
from org.sleuthkit.autopsy.casemodule.services import Blackboard
from org.sleuthkit.autopsy.datamodel import ContentUtils
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.datamodel import TskData
#custom imports
import sys
import binascii
import re
import subprocess
import tempfile

ModelFilePath = "models/deepspeech.pbmm"
ScorerFilePath = "models/deepspeech.scorer"
beam_width = "100"
lm_alpha = "0.93"
lm_beta = "1.18"
enableVAD = "1"
vadStrictness = "3"

def findLen(str1):
    counter = 0    
    for i in str1:
        counter += 1
    return counter

def int2hex(number, bits):
    """ Return the 2'complement hexadecimal representation of a number """

    if number < 0:
        return hex((1 << bits) + number)
    else:
        return hex(number)

# Factory that defines the name and details of the module and allows Autopsy
# to create instances of the modules that will do the analysis.
class AudioToTextModuleFactory(IngestModuleFactoryAdapter):

    def __init__(self):
        self.settings = None

    # TODO: give it a unique name.  Will be shown in module list, logs, etc.
    moduleName = "Trying Hardest - AudioToText"

    def getModuleDisplayName(self):
        return self.moduleName

    # TODO: Give it a description
    def getModuleDescription(self):
        return "This module utilizes DeepSpeech to convert audio to text."
    
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

    # Return true if module wants to get called for each file
    def isFileIngestModuleFactory(self):
        return True

    # can return null if isFileIngestModuleFactory returns false
    def createFileIngestModule(self, ingestOptions):
        return AudioToTextModule(self.settings)

# Data Source-level ingest module.  One gets created per data source.
class AudioToTextModule(FileIngestModule):

    _logger = Logger.getLogger(AudioToTextModuleFactory.moduleName)

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
        self.filesFound = 0
        self.context = context

        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        # raise IngestModuleException(IngestModule(), "Oh No!")
        pass

    # Where the analysis is done.
    # The 'dataSource' object being passed in is of type org.sleuthkit.datamodel.Content.
    # See:x http://www.sleuthkit.org/sleuthkit/docs/jni-docs/interfaceorg_1_1sleuthkit_1_1datamodel_1_1_content.html
    # 'progressBar' is of type org.sleuthkit.autopsy.ingest.DataSourceIngestModuleProgress
    # See: http://sleuthkit.org/autopsy/docs/api-docs/3.1/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_data_source_ingest_module_progress.html
    def process(self, file):

        global ModelFilePath
        global ScorerFilePath
        global beam_width
        global lm_alpha
        global lm_beta
        global enableVAD
        global vadStrictness

        # Skip non-files
        if ((file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNALLOC_BLOCKS) or
            (file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNUSED_BLOCKS) or
            (file.isFile() == False)):
            return IngestModule.ProcessResult.OK
        # Use blackboard class to index blackboard artifacts for keyword search
        blackboard = Case.getCurrentCase().getServices().getBlackboard()

        # For an example, we will flag files with .wav in the name and make a blackboard artifact.
        if file.getName().lower().endswith(".wav") or file.getName().lower().endswith(".mp3"):            
            self.log(Level.INFO, "DEBUG3")            

            self.log(Level.INFO, "Found an audio file: " + file.getName())
            self.filesFound+=1

            ##Extract audio begins here
            inputStream = ReadContentInputStream(file)
            buffer = jarray.zeros(file.getSize(), "b")            
            len = inputStream.read(buffer)

            #remove unneccessary characters 
            buffer = str(buffer)
            buffer=re.sub("array.*\\[",'',buffer)
            buffer=re.sub(" ",'',buffer)                   
            buffer=re.sub("]\\)",'',buffer)
            buffer = list(buffer.split(","))
            buffer = [int(x) for x in buffer]

            file_dir = os.path.dirname(os.path.abspath(__file__))
            tempFile = os.path.join(file_dir, str(file.getName()))

            #Save bytes into audio file 
            with open(tempFile, 'wb') as f:
                #convert bytes into hex, output hex to file
                for value in buffer:
                    hexValue = (str(int2hex(int(value),8))[2:])                    
                    if findLen(hexValue) == 1:
                        hexValue = "0"+hexValue
                    f.write(str(binascii.unhexlify(hexValue)))

            #Call python script                      
            #commandToCall = 'python AudioToText.py ' + '\"' + str(file.getName()) + '\"'
            commandToCall = 'python AudioToText.py' + ' \"' + ModelFilePath + '\"' + ' \"' + ScorerFilePath + '\"' + ' ' + beam_width + ' ' + lm_alpha + ' ' + lm_beta +  ' ' + enableVAD + ' ' + vadStrictness + ' \"' + str(file.getName()) + '\"'
            try: 
                transcript = subprocess.check_output(commandToCall, shell=True, cwd=file_dir)
            except: 
                transcript = "Error"
            
            os.remove(tempFile)

            if transcript.strip().decode("utf-8") == 'Does not contain any speech.' or transcript.strip().decode("utf-8") == 'Errors':
                return IngestModule.ProcessResult.OK

            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artifact.  Refer to the developer docs for other examples.
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME,
                  AudioToTextModuleFactory.moduleName, "Audio with Speech Found")
            attId = blackboard.getOrAddAttributeType("TranscribedText", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Transcribed Text")
            atribute=BlackboardAttribute(attId, AudioToTextModuleFactory.moduleName, transcript.strip().decode("utf-8"))
            art.addAttribute(att)
            art.addAttribute(atribute)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())

            # Fire an event to notify the UI and others that there is a new artifact
            IngestServices.getInstance().fireModuleDataEvent(
                ModuleDataEvent(AudioToTextModuleFactory.moduleName,
                    BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT, None))

            # For the example (this wouldn't be needed normally), we'll query the blackboard for data that was added
            # by other modules. We then iterate over its attributes.  We'll just print them, but you would probably
            # want to do something with them.
            artifactList = file.getArtifacts(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            self.log(Level.SEVERE, "DEBUG artifact:" + str(artifactList))
            for artifact in artifactList:
                attributeList = artifact.getAttributes()
                for attrib in attributeList:
                    self.log(Level.INFO, attrib.toString())

        return IngestModule.ProcessResult.OK

    # Where any shutdown code is run and resources are freed.
    # TODO: Add any shutdown code that you need here.
    def shutDown(self):
        # As a final part of this example, we'll send a message to the ingest inbox with the number of files found (in this thread)
        message = IngestMessage.createMessage(
            IngestMessage.MessageType.DATA, AudioToTextModuleFactory.moduleName,
                str(self.filesFound) + " files found")
        ingestServices = IngestServices.getInstance().postMessage(message)    


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
        global ModelFilePath
        chooseFile = JFileChooser()
        filter = FileNameExtensionFilter(".pbmm", ["pbmm"])
        chooseFile.setAcceptAllFileFilterUsed(False);
        chooseFile.setFileFilter(filter)

        ret = chooseFile.showDialog(self.panel0, "Select Model File")
        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            Canonical_file = file.getCanonicalPath()
            self.ModelFile_TF.setText(Canonical_file)
            ModelFilePath = Canonical_file

    # Select Scorer File onClick Event
    def selectScorerFile(self, e):
        global ScorerFilePath
        chooseFile = JFileChooser()
        filter = FileNameExtensionFilter(".scorer", ["scorer"])
        chooseFile.setAcceptAllFileFilterUsed(False);
        chooseFile.setFileFilter(filter)

        ret = chooseFile.showDialog(self.panel0, "Select Scorer File")
        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            Canonical_file = file.getCanonicalPath()
            self.ScorerFile_TF.setText(Canonical_file)
            ScorerFilePath = Canonical_file

    # Modify beam_width field event
    def beam_width_mod(self, e):
        global beam_width
        beam_width = self.beam_width_TF.getText()

    # Modify lm_alpha field event
    def lm_alpha_mod(self, e):
        global lm_alpha
        lm_alpha = self.lm_alpha_TF.getText()

    # Modify lm_beta field event
    def lm_beta_mod(self, e):
        global lm_beta
        lm_beta = self.lm_beta_TF.getText()

    # Check if VAD is enabled
    def checkVAD(self, e):
        global enableVAD
        if self.vad_CheckBox.isSelected():
            enableVAD = "1"
            self.vad_TF.setEnabled(True)
        else:
            enableVAD = "0"
            self.vad_TF.setEnabled(False)

    # Modify VAD Verbosity Event
    def modifyVAD(self, e):
        global vadStrictness
        vadStrictness = self.vad_TF.getText()

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

        self.lm_alpha_TF = JTextField("0.93",20)
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

        self.lm_beta_TF = JTextField("1.18",20)
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
        self.vad_CheckBox = JCheckBox( "Enable VAD (0-3)", actionPerformed=self.checkVAD)
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

        self.vad_TF = JTextField("3",20)
        self.vad_TF.getDocument().insertUpdate = self.modifyVAD
        self.vad_TF.getDocument().removeUpdate = self.modifyVAD
        self.vad_TF.getDocument().changedUpdate = self.modifyVAD
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 31
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.vad_TF, self.gbcPanel0 ) 
        self.panel0.add( self.vad_TF ) 

        self.add(self.panel0)

    # TODO: Update this for your UI
    def customizeComponents(self):
        pass

    # Return the settings used
    def getSettings(self):
        return self.local_settings

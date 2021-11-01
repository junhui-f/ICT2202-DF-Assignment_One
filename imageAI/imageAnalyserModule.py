import jarray
import inspect
import os
from subprocess import Popen, PIPE

from javax.swing import JCheckBox
from javax.swing import JButton
from javax.swing import ButtonGroup
from javax.swing import JComboBox
#from javax.swing import JRadioButton
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
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.datamodel import TskData
#custom imports
import sys
import binascii
import re
import subprocess
import tempfile
from subprocess import check_output

tempDir = tempfile.gettempdir() + "\\extracted_images\\"
imageAIScriptFilePath = os.path.dirname(os.path.abspath(__file__)) + "\\detect.py"
facialRecScriptFilePath = os.path.dirname(os.path.abspath(__file__)) + "\\detectFace.py"
doFacialRec = False
facialRecTargetImgPath = "default"

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

def cleanUp():
    #remove images in temp
    for file in os.listdir(tempDir):
        if file.endswith('.jpg') or file.endswith('.JPG'):
            os.remove(tempDir+file)

# Factory that defines the name and details of the module and allows Autopsy
# to create instances of the modules that will do the analysis.
class ImageAIModuleFactory(IngestModuleFactoryAdapter):

    def __init__(self):
        self.settings = None

    moduleName = "Trying Hardest - Image Analyser"
    
    def getModuleDisplayName(self):
        return self.moduleName
    
    def getModuleDescription(self):
        return "This modile utilizes imageAI to detect objects within images and Facial Recognition to search for specific person through the images found"
    
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

    def isFileIngestModuleFactory(self):
        return True

    def createFileIngestModule(self, ingestOptions):
        return ImageAIModule(self.settings)

# Data Source-level ingest module.  One gets created per data source.
class ImageAIModule(FileIngestModule):

    _logger = Logger.getLogger(ImageAIModuleFactory.moduleName)

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
        
        Combo_Box_entry = self.local_settings.getSetting('ComboBox')
        self.log(Level.INFO, "Combo Box Entry Starts here =====>")
        self.log(Level.INFO, self.local_settings.getSetting('ComboBox'))
        self.log(Level.INFO, "<====== Combo Box Entry Ends here")
        
        # list_box_entry = self.local_settings.getSetting('ListBox').split(",")
        # self.log(Level.INFO, "List Box Entry Starts here =====>")
        # self.log(Level.INFO, str(list_box_entry))
        # for num in range (0, len(list_box_entry)):
        #    self.log(Level.INFO, str(list_box_entry[num]))
        # self.log(Level.INFO, "<====== List Box Entry Ends here")

        # Check to see if the file to import exists, if it does not then raise an exception and log error
        if self.local_settings.getSetting('Imp_File_Flag') == 'true':
            self.log(Level.INFO, self.local_settings.getSetting('File_Imp_TF'))
            self.path_to_import_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.local_settings.getSetting('File_Imp_TF'))
            if not os.path.exists(self.path_to_import_file):
               raise IngestModuleException("File to import is not available")
        
        if self.local_settings.getSetting('Facial_Rec_Flag') == 'true':
            self.log(Level.INFO, self.local_settings.getSetting('ExecFile'))
            self.path_to_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.local_settings.getSetting('ExecFile'))
            if not os.path.exists(self.path_to_exe):
               raise IngestModuleException("File to Run/execute does not exist.")
        
        
        #self.logger.logp(Level.INFO, GUI_TestWithUI.__name__, "startUp", str(self.List_Of_Events))
        #self.log(Level.INFO, str(self.List_Of_GUI_Test))
        
        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        # raise IngestModuleException(IngestModule(), "Oh No!")
        pass

    # Where the analysis is done.
    # The 'dataSource' object being passed in is of type org.sleuthkit.datamodel.Content.
    # See:x http://www.sleuthkit.org/sleuthkit/docs/jni-docs/interfaceorg_1_1sleuthkit_1_1datamodel_1_1_content.html
    # 'progressBar' is of type org.sleuthkit.autopsy.ingest.DataSourceIngestModuleProgress
    # See: http://sleuthkit.org/autopsy/docs/api-docs/3.1/classorg_1_1sleuthkit_1_1autopsy_1_1ingest_1_1_data_source_ingest_module_progress.html
    def process(self, file):
        #globals to check if checkbox is ticked and get file path of selected image
        global doFacialRec
        global facialRecTargetImgPath
    
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)

        # Skip non-files
        if ((file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNALLOC_BLOCKS) or
            (file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNUSED_BLOCKS) or
            (file.isFile() == False)):
            return IngestModule.ProcessResult.OK

        # Use blackboard class to index blackboard artifacts for keyword search
        blackboard = Case.getCurrentCase().getServices().getBlackboard()

        # flag files that ends with jpg, png, gif, jpeg
        if file.getName().lower().endswith(".jpg") or file.getName().lower().endswith(".png") or file.getName().lower().endswith(".gif") or file.getName().lower().endswith(".png") or file.getName().lower().endswith(".jpeg"):
            self.log(Level.INFO, "DEBUG3")

            self.log(Level.INFO, "Found an image file: " + file.getName())
            self.log(Level.INFO, "debugging imageAIScriptFilePath: " + imageAIScriptFilePath)
            self.filesFound+=1

            ##Extract images begins here
            inputStream = ReadContentInputStream(file)
            buffer = jarray.zeros(file.getSize(), "b")
            len = inputStream.read(buffer)

            #remove uneccessary characters
            buffer = str(buffer)
            buffer=re.sub("array.*\\[",'',buffer)
            buffer=re.sub(" ",'',buffer)
            buffer=re.sub("]\\)",'',buffer)
            buffer = list(buffer.split(","))
            buffer = [int(x) for x in buffer]

            #Save bytes into image file
            with open(tempDir+str(file.getName()), 'wb') as f:
                #convert bytes into hex, output hex to file
                for value in buffer:
                    hexValue = (str(int2hex(int(value),8))[2:])
                    if findLen(hexValue) == 1:
                        hexValue = "0"+hexValue
                        f.write(str(binascii.unhexlify(hexValue)))
                    else:
                        f.write(str(binascii.unhexlify(hexValue)))

            #Call the imageAI script
            fileName = str(file.getName())
            imgResultStdOut = check_output(['python', imageAIScriptFilePath, fileName, tempDir])

            if str(imgResultStdOut) == '':
                imgResultStdOut = 'Unknown'
        
            #Call the facial recognition script
            facialRecStdOut = "default facialRecStdOut"
            if doFacialRec is True:
                #call the facial_rec.py script
                facialRecStdOut = check_output(['python', facialRecScriptFilePath, facialRecTargetImgPath, tempDir, fileName])

            ##Process the output folder to obtain the tags
            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artifact.  Refer to the developer docs for other examples.
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME,
                  ImageAIModuleFactory.moduleName, "Image analysed")

            attId = blackboard.getOrAddAttributeType("Image analysis", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Image analysis")
            atribute = BlackboardAttribute(attId, ImageAIModuleFactory.moduleName, str(imgResultStdOut))            
            art.addAttribute(atribute)

            if doFacialRec is True:
                attId2 = blackboard.getOrAddAttributeType("Facial recognition", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Facial recognition")
                atribute2 = BlackboardAttribute(attId2, ImageAIModuleFactory.moduleName, str(facialRecStdOut))
                art.addAttribute(atribute2)                

            art.addAttribute(att)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())

            # Fire an event to notify the UI and others that there is a new artifact
            IngestServices.getInstance().fireModuleDataEvent(
                ModuleDataEvent(ImageAIModuleFactory.moduleName,
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

            # #debugging
            # f = open(r'C:\users\kevin\desktop\debug.txt', 'a')
            # f.write('filname:'+fileName + '\n' + str(doFacialRec) + '\nfacialRecTargetImgPath' + str(facialRecTargetImgPath) + '\nFacialRecStdout:' + facialRecStdOut)
            # f.close()

        return IngestModule.ProcessResult.OK              
        
    # Where any shutdown code is run and resources are freed.
    # TODO: Add any shutdown code that you need here.
    def shutDown(self):
        # As a final part of this example, we'll send a message to the ingest inbox with the number of files found (in this thread)
        message = IngestMessage.createMessage(
            IngestMessage.MessageType.DATA, ImageAIModuleFactory.moduleName,
                str(self.filesFound) + " files found")
        ingestServices = IngestServices.getInstance().postMessage(message)
        cleanUp()

        
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
    
    # TODO: Update this for your UI
    def checkBoxEvent(self, event):
        global doFacialRec
        if self.Exec_Program_CB.isSelected():
            self.local_settings.setSetting('Facial_Rec_Flag', 'true')
            self.Program_Executable_TF.setEnabled(True)
            self.Find_Program_Exec_BTN.setEnabled(True)
            doFacialRec = True
        else:
            self.local_settings.setSetting('Facial_Rec_Flag', 'false')
            self.Program_Executable_TF.setText("")
            self.Program_Executable_TF.setEnabled(False)
            self.Find_Program_Exec_BTN.setEnabled(False)
            doFacialRec = False

    def keyPressed(self, event):
        self.local_settings.setSetting('Area', self.area.getText()) 

    def onchange_cb(self, event):
        self.local_settings.setSetting('ComboBox', event.item) 
        #self.Error_Message.setText(event.item)

    def onchange_lb(self, event):
        self.local_settings.setSetting('ListBox', "")
        list_selected = self.List_Box_LB.getSelectedValuesList()
        self.local_settings.setSetting('ListBox', str(list_selected))      

    def onClick(self, e):
       global facialRecTargetImgPath    
       chooseFile = JFileChooser()

       ret = chooseFile.showDialog(self.panel0, "Select Target Face Image")

       if ret == JFileChooser.APPROVE_OPTION:
           file = chooseFile.getSelectedFile()
           Canonical_file = file.getCanonicalPath()
           #text = self.readPath(file)
           # if self.File_Imp_TF.isEnabled():
              # self.File_Imp_TF.setText(Canonical_file)
              # self.local_settings.setSetting('File_Imp_TF', Canonical_file)
           # else:
           self.local_settings.setSetting('ExecFile', Canonical_file)
           self.Program_Executable_TF.setText(Canonical_file)
           facialRecTargetImgPath = Canonical_file

    # TODO: Update this for your UI
    def initComponents(self):
        self.panel0 = JPanel()

        self.rbgPanel0 = ButtonGroup() 
        self.gbPanel0 = GridBagLayout() 
        self.gbcPanel0 = GridBagConstraints() 
        self.panel0.setLayout( self.gbPanel0 ) 

        self.Exec_Program_CB = JCheckBox("Targeted Facial Recognition", actionPerformed=self.checkBoxEvent)
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 1 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Exec_Program_CB, self.gbcPanel0 ) 
        self.panel0.add( self.Exec_Program_CB ) 

        self.Program_Executable_TF = JTextField(20) 
        self.Program_Executable_TF.setEnabled(True)
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 3 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Program_Executable_TF, self.gbcPanel0 ) 
        self.panel0.add( self.Program_Executable_TF ) 

        self.Find_Program_Exec_BTN = JButton( "Select", actionPerformed=self.onClick)
        self.Find_Program_Exec_BTN.setEnabled(True)
        self.rbgPanel0.add( self.Find_Program_Exec_BTN ) 
        self.gbcPanel0.gridx = 6 
        self.gbcPanel0.gridy = 3 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Find_Program_Exec_BTN, self.gbcPanel0 ) 
        self.panel0.add( self.Find_Program_Exec_BTN ) 
        
        self.add(self.panel0)

    # TODO: Update this for your UI
    def customizeComponents(self):
        pass
        # self.Exec_Program_CB.setSelected(self.local_settings.getSetting('Facial_Rec_Flag') == 'true')

    # Return the settings used
    def getSettings(self):
        return self.local_settings

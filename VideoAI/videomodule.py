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
from java.lang import System
from java.util.logging import Level
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.datamodel import TskData
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.ingest import ModuleDataEvent
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.casemodule.services import Blackboard
# custom imports
import sys
import os, subprocess
import binascii
import re


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
# to create instances of the modules that will do the anlaysis.
# TODO: Rename this to something more specific.  Search and replace for it because it is used a few times
class VideoModuleFactory(IngestModuleFactoryAdapter):
    # TODO: give it a unique name.  Will be shown in module list, logs, etc.
    moduleName = "Trying Hardest - VideoAnalysis"

    def getModuleDisplayName(self):
        return self.moduleName

    # TODO: Give it a description
    def getModuleDescription(self):
        return "This module utilizes imageai to analysis object in video."

    def getModuleVersionNumber(self):
        return "1.0"

    # Return true if module wants to get called for each file
    def isFileIngestModuleFactory(self):
        return True

    # can return null if isFileIngestModuleFactory returns false
    def createFileIngestModule(self, ingestOptions):
        return VideoModule()


# File-level ingest module.  One gets created per thread.
# TODO: Rename this to something more specific. Could just remove "Factory" from above name.
# Looks at the attributes of the passed in file.
class VideoModule(FileIngestModule):
    _logger = Logger.getLogger(VideoModuleFactory.moduleName)

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def startUp(self, context):
        self.filesFound = 0
        pass
    def process(self, file):
        # Skip non-files
        if ((file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNALLOC_BLOCKS) or
                (file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNUSED_BLOCKS) or
                (file.isFile() == False)):
            return IngestModule.ProcessResult.OK
        # Use blackboard class to index blackboard artifacts for keyword search
        blackboard = Case.getCurrentCase().getServices().getBlackboard()

        # For an example, we will flag files with .wav in the name and make a blackboard artifact.
        if file.getName().lower().endswith(".mp4"):
            self.log(Level.INFO, "DEBUG3")

            self.log(Level.INFO, "Found an video file: " + file.getName())
            self.filesFound += 1

            ##Extract video begins here
            inputStream = ReadContentInputStream(file)
            buffer = jarray.zeros(file.getSize(), "b")
            len = inputStream.read(buffer)

            # remove unneccessary characters
            buffer = str(buffer)
            buffer = re.sub("array.*\\[", '', buffer)
            buffer = re.sub(" ", '', buffer)
            buffer = re.sub("]\\)", '', buffer)
            buffer = list(buffer.split(","))
            buffer = [int(x) for x in buffer]

            file_dir = os.path.dirname(os.path.abspath(__file__))
            tempFile = os.path.join(file_dir, str(file.getName()))

            # Save bytes into video file
            with open(tempFile, 'wb') as f:
                # convert bytes into hex, output hex to file
                for value in buffer:
                    hexValue = (str(int2hex(int(value), 8))[2:])
                    if findLen(hexValue) == 1:
                        hexValue = "0" + hexValue
                    f.write(str(binascii.unhexlify(hexValue)))

            # Call python script
            commandToCall = 'python videoDetection.py ' + '\"' + str(file.getName()) + '\"'
            try:
                #transcript = check_output(['python', 'videoDetection.py', str(file.getName())])
                transcript = subprocess.check_output(commandToCall, shell=True, cwd=file_dir)
            except:
                transcript = "Error"

            os.remove(tempFile)

            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artifact.  Refer to the developer docs for other examples.
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME,
                                      VideoModuleFactory.moduleName, "Video analysis finish")
            attId = blackboard.getOrAddAttributeType("Objects Found",
                                                     BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING,
                                                     "Objects Found")
            atribute = BlackboardAttribute(attId, VideoModuleFactory.moduleName,transcript.strip().decode("utf-8"))

            art.addAttribute(att)
            art.addAttribute(atribute)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())

            # Fire an event to notify the UI and others that there is a new artifact
            IngestServices.getInstance().fireModuleDataEvent(
                ModuleDataEvent(VideoModuleFactory.moduleName,
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
            IngestMessage.MessageType.DATA, VideoModuleFactory.moduleName,
            str(self.filesFound) + " files found")
        ingestServices = IngestServices.getInstance().postMessage(message)
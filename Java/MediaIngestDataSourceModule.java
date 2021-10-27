/*
 * Sample module in the public domain.  Feel free to use this as a template
 * for your modules.
 * 
 *  Contact: Brian Carrier [carrier <at> sleuthkit [dot] org]
 *
 *  This is free and unencumbered software released into the public domain.
 *  
 *  Anyone is free to copy, modify, publish, use, compile, sell, or
 *  distribute this software, either in source code form or as a compiled
 *  binary, for any purpose, commercial or non-commercial, and by any
 *  means.
 *  
 *  In jurisdictions that recognize copyright laws, the author or authors
 *  of this software dedicate any and all copyright interest in the
 *  software to the public domain. We make this dedication for the benefit
 *  of the public at large and to the detriment of our heirs and
 *  successors. We intend this dedication to be an overt act of
 *  relinquishment in perpetuity of all present and future rights to this
 *  software under copyright law.
 *  
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 *  IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 *  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 *  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 *  OTHER DEALINGS IN THE SOFTWARE. 
 */

package ICT.DF.TryingHardest;

import java.util.List;
import java.util.logging.Level;
import org.sleuthkit.autopsy.casemodule.Case;
import org.sleuthkit.autopsy.casemodule.NoCurrentCaseException;
import org.sleuthkit.autopsy.casemodule.services.FileManager;
import org.sleuthkit.autopsy.ingest.DataSourceIngestModuleProgress;
import org.sleuthkit.autopsy.ingest.IngestModule;
import org.sleuthkit.datamodel.AbstractFile;
import org.sleuthkit.datamodel.Content;
import org.sleuthkit.datamodel.TskCoreException;
import org.sleuthkit.autopsy.coreutils.Logger;
import org.sleuthkit.autopsy.ingest.DataSourceIngestModule;
import org.sleuthkit.autopsy.ingest.IngestJobContext;
import org.sleuthkit.autopsy.ingest.IngestMessage;
import org.sleuthkit.autopsy.ingest.IngestServices;
import org.sleuthkit.datamodel.TskData;

class MediaIngestDataSourceModule implements DataSourceIngestModule {

    private final boolean imageAnalysisChoice;
    private IngestJobContext context = null;

    MediaIngestDataSourceModule(MediaIngestModuleJobSettings settings) {
        this.imageAnalysisChoice = settings.getImageAnalysisChoice();
    }

    @Override
    public void startUp(IngestJobContext context) throws IngestModuleException {
        this.context = context;
    }

    @Override
    public ProcessResult process(Content dataSource, DataSourceIngestModuleProgress progressBar) {
        System.out.println("OK - DATA SOURCE");
        // There are two tasks to do.
        progressBar.switchToDeterminate(2);

        // If Image Analysis sslected
        if (imageAnalysisChoice == true) {
            try {
                // Get count of files with .doc extension.
                FileManager fileManager = Case.getCurrentCaseThrows().getServices().getFileManager();
                List<AbstractFile> pngFiles = fileManager.findFiles(dataSource, "%.png");
                List<AbstractFile> jpgFiles = fileManager.findFiles(dataSource, "%.jpg");

                long pngFileCount = 0;
                for (AbstractFile pngFile : pngFiles) {
                    if (!imageAnalysisChoice || pngFile.getKnown() != TskData.FileKnown.KNOWN) {
                        ++pngFileCount;
                    }
                }

                long jpgFileCount = 0;
                for (AbstractFile jpgFile : jpgFiles) {
                    if (!imageAnalysisChoice || jpgFile.getKnown() != TskData.FileKnown.KNOWN) {
                        ++jpgFileCount;
                    }
                }

                progressBar.progress(1);

                // check if we were cancelled
                if (context.dataSourceIngestIsCancelled()) {
                    return IngestModule.ProcessResult.OK;
                }

                // Post a message to the ingest messages in box.
                String pngText = String.format("Found %d PNG files!", pngFileCount);
                String jpgText = String.format("Found %d JPG files!", jpgFileCount);

                IngestMessage pngMessage = IngestMessage.createMessage(
                        IngestMessage.MessageType.DATA,
                        MediaIngestModuleFactory.getModuleName(),
                        pngText);
                IngestServices.getInstance().postMessage(pngMessage);

                IngestMessage jpgMessage = IngestMessage.createMessage(
                        IngestMessage.MessageType.DATA,
                        MediaIngestModuleFactory.getModuleName(),
                        jpgText);
                IngestServices.getInstance().postMessage(jpgMessage);

                return IngestModule.ProcessResult.OK;

            } catch (TskCoreException | NoCurrentCaseException ex) {
                IngestServices ingestServices = IngestServices.getInstance();
                Logger logger = ingestServices.getLogger(MediaIngestModuleFactory.getModuleName());
                logger.log(Level.SEVERE, "File query failed", ex);
                return IngestModule.ProcessResult.ERROR;
            }
        } else {
            return IngestModule.ProcessResult.OK;
        }

    }
}
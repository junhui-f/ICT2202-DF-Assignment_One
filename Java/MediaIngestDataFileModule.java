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

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.logging.Level;
import org.sleuthkit.autopsy.coreutils.Logger;
import org.sleuthkit.autopsy.ingest.FileIngestModule;
import org.sleuthkit.autopsy.ingest.IngestJobContext;
import org.sleuthkit.autopsy.ingest.IngestMessage;
import org.sleuthkit.autopsy.ingest.IngestModule;
import org.sleuthkit.autopsy.ingest.IngestModuleReferenceCounter;
import org.sleuthkit.autopsy.ingest.IngestServices;
import org.sleuthkit.datamodel.AbstractFile;
import org.sleuthkit.datamodel.Blackboard;
import org.sleuthkit.datamodel.BlackboardArtifact;
import org.sleuthkit.datamodel.BlackboardAttribute;
import org.sleuthkit.datamodel.TskCoreException;
import org.sleuthkit.datamodel.TskData;

/**
 * Sample file ingest module that doesn't do much. Demonstrates per ingest job
 * module settings, use of a subset of the available ingest services and
 * thread-safe sharing of per ingest job data.
 */
class MediaIngestDataFileModule implements FileIngestModule {

    private static final HashMap<Long, Long> artifactCountsForIngestJobs = new HashMap<>();
    private static final BlackboardAttribute.ATTRIBUTE_TYPE ATTR_TYPE = BlackboardAttribute.ATTRIBUTE_TYPE.TSK_COUNT;
    private final boolean imageAnalysisChoice;
    private IngestJobContext context = null;
    private static final IngestModuleReferenceCounter refCounter = new IngestModuleReferenceCounter();
    private final Set<String> validIMGExtensions = new HashSet<String>() {{
        add("png");
        add("jpg");
    }};


    MediaIngestDataFileModule(MediaIngestModuleJobSettings settings) {
        this.imageAnalysisChoice = settings.getImageAnalysisChoice();
    }

    @Override
    public void startUp(IngestJobContext context) throws IngestModuleException {
        this.context = context;
        refCounter.incrementAndGet(context.getJobId());
    }

    @Override
    public IngestModule.ProcessResult process(AbstractFile file) {

        // If Image Analysis sslected
        if (imageAnalysisChoice == true) {
            // Skip anything other than actual file system files.
            // Skip if not defined in validIMGExtensions
            if ((file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNALLOC_BLOCKS)
                || (file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.UNUSED_BLOCKS)
                || (file.isFile() == false)
                || (validIMGExtensions.contains((file.getNameExtension()).toLowerCase())) == false) {
                System.out.println("NOT OK - DATA FILE - " + file.getName());
                return IngestModule.ProcessResult.OK;
            }

            System.out.println("OK - DATA FILE - " + file.getName());

            try {
                int count1 = 1;

                // Make an attribute using the ID for the attribute attrType that 
                // was previously created.
                BlackboardAttribute attr = new BlackboardAttribute(ATTR_TYPE, MediaIngestModuleFactory.getModuleName(), count1);
                // Add the to the general info artifact for the file. In a
                // real module, you would likely have more complex data types 
                // and be making more specific artifacts.
                BlackboardArtifact art = file.getGenInfoArtifact();
                art.addAttribute(attr);

                // This method is thread-safe with per ingest job reference counted
                // management of shared data.
                addToBlackboardPostCount(context.getJobId(), 1L);

                /*
                 * post the artifact which will index the artifact for keyword
                 * search, and fire an event to notify UI of this new artifact
                 */
                file.getSleuthkitCase().getBlackboard().postArtifact(art, MediaIngestModuleFactory.getModuleName());

                return IngestModule.ProcessResult.OK;

            } catch (TskCoreException | Blackboard.BlackboardException ex) {
                IngestServices ingestServices = IngestServices.getInstance();
                Logger logger = ingestServices.getLogger(MediaIngestModuleFactory.getModuleName());
                logger.log(Level.SEVERE, "Error processing file (id = " + file.getId() + ")", ex);
                return IngestModule.ProcessResult.ERROR;
            }
        } else {
            return IngestModule.ProcessResult.OK;
        }
        
    }

    @Override
    public void shutDown() {
        // This method is thread-safe with per ingest job reference counted
        // management of shared data.
        reportBlackboardPostCount(context.getJobId());
    }

    synchronized static void addToBlackboardPostCount(long ingestJobId, long countToAdd) {
        Long fileCount = artifactCountsForIngestJobs.get(ingestJobId);

        // Ensures that this job has an entry
        if (fileCount == null) {
            fileCount = 0L;
            artifactCountsForIngestJobs.put(ingestJobId, fileCount);
        }

        fileCount += countToAdd;
        artifactCountsForIngestJobs.put(ingestJobId, fileCount);
    }

    synchronized static void reportBlackboardPostCount(long ingestJobId) {
        Long refCount = refCounter.decrementAndGet(ingestJobId);
        if (refCount == 0) {
            Long filesCount = artifactCountsForIngestJobs.remove(ingestJobId);
            String msgText = String.format("Posted %d times to the blackboard", filesCount);
            IngestMessage message = IngestMessage.createMessage(
                    IngestMessage.MessageType.INFO,
                    MediaIngestModuleFactory.getModuleName(),
                    msgText);
            IngestServices.getInstance().postMessage(message);
        }
    }
}

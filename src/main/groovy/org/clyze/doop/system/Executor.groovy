package org.clyze.doop.system

import groovy.transform.TypeChecked
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory

import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

@TypeChecked
class Executor {

    protected Log logger = LogFactory.getLog(getClass())

    static final Closure STDOUT_PRINTER = { String line -> println line }

    Map<String, String> environment

    Executor(Map<String, String> environment) {
        this.environment = environment
    }

    void execute(String workingDirectory,
                 String commandLine,
                 Closure outputLineProcessor = STDOUT_PRINTER) {

        def pb = new ProcessBuilder("/bin/bash", "-c", commandLine)
        if (workingDirectory) {
            File cwd = FileOps.findDirOrThrow(workingDirectory, "Working directory is invalid: $workingDirectory")
            pb.directory(cwd)
        }
        pb.redirectErrorStream(true)
        def environment = pb.environment()
        environment.clear()
        environment.putAll(this.environment)
        def process = pb.start()

        final InputStream is = process.getInputStream()
        //final InputStream es = process.getErrorStream()

        ExecutorService executorService = Executors.newSingleThreadExecutor()

        // Add a shutdown hook in case the JVM terminates during the execution of the process
        def shutdownActions = {
            logger.debug("Destroying process: $commandLine")
            process.destroy()
            logger.debug("Process destroyed: $commandLine")
            executorService.shutdownNow()
        }
        def shutdownThread = new Thread(shutdownActions as Runnable)
        Runtime.getRuntime().addShutdownHook(shutdownThread)

        /*
         * Put the use of readline in a separate thread because it ignores
         * thread interrupts. When an interrupt occurs, the "parent" thread
         * will handle it and destroy the process so that the underlying socket
         * is closed and readLine will fail. Otherwise if when a timeout
         * occurs, the process will continue to run ignoring any attempt to
         * stop it.
         */
        try {
            executorService.submit(new Runnable() {
                @Override
                void run() {
                    is.newReader().withReader { reader ->
                        String nextLine;

                        while ((nextLine = reader.readLine()) != null) {
                            outputLineProcessor(nextLine.trim());
                        }
                    }
                }
            }).get()
        }
        catch (InterruptedException e) {
            Runtime.getRuntime().removeShutdownHook(shutdownThread)
            shutdownActions.call()
            throw e
        }
        finally {
            executorService.shutdownNow()
        }
        Runtime.getRuntime().removeShutdownHook(shutdownThread)

        // Wait for process to terminate
        def returnCode = process.waitFor()

        // Create an error string that contains everything in the stderr stream
        //def errorMessages = es.getText()
        //if (!errorMessages.isAllWhitespace()) {
        //    System.err.print(errorMessages)
        //}

        // Check return code and raise exception at failure indication
        if (returnCode != 0) {
            throw new RuntimeException("Command exited with non-zero status:\n $commandLine")
        }
    }

    void execute(String commandLine, Closure outputLineProcessor = STDOUT_PRINTER) {
        execute(null, commandLine, outputLineProcessor)
    }
}

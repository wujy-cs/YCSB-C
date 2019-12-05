import funcs
import sys
import os

dbPath = "/mnt/expdb/"
backupPath = "/mnt/backup/"
#dbPath = "/mnt/raidstore/"
valueSizes = ["zipfcorea","zipfcoreb","zipfcorec","zipfcored","zipfcoree","zipfcoref"]
dbSize = "300GB"
smallThresh = 64
midThresh = 30000
for valueSize in valueSizes:
    dbfilename = dbPath+"titandb_vtablenolarge"+valueSize+dbSize
    backupfilename = backupPath+"titandb_vtablenolarge"+valueSize+dbSize
    workload = "./workloads/workload"+valueSize+dbSize+".spec"
    memtable = 64
    resultfile = "./resultDir/vtablenolarge"+valueSize+dbSize+"memtable"+str(memtable)
    sepBeforeFlush = "false"
    if sepBeforeFlush == "true":
        resultfile = resultfile + "before"
    
    
    configs = {
        "bloomBits":"10",
        "seekCompaction":"false",
        "directIO":"false",
        "compression":"false",
        "noCompaction":"false",
        "blockCache":str(8*1024*1024),
        "memtable":str(memtable*1024*1024),
        "numThreads":str(8),
        "tiered":"false",
        "levelMerge":"true",
        "rangeMerge":"true",
        "sepBeforeFlush":sepBeforeFlush,
        "midThresh":str(midThresh),
        "smallThresh":str(smallThresh)
    }
    
    phase = sys.argv[1]
    
    if __name__ == '__main__':
        #set configs
        os.system("sync && echo 3 > /proc/sys/vm/drop_caches")
    
        if phase=="load":
            configs["noCompaction"] = "false"
            
        for cfg in configs:
            funcs.modifyConfig("./configDir/leveldb_config.ini","config",cfg,configs[cfg])
    
        for cfg in configs:
            funcs.modifyConfig("./configDir/leveldb_config.ini","config",cfg,configs[cfg])
    
        if len(sys.argv) == 3:
            resultfile = sys.argv[2]
    
        if phase=="load":
            resultfile = resultfile+"_load"
            funcs.load("titandb",dbfilename,workload,resultfile)
    
        if phase=="run":
            os.system("sudo rm -rf {0}".format(dbfilename))
            os.system("sudo cp -r {0} {1}".format(backupfilename, dbPath))
            resultfile = resultfile+"_run"
            print(resultfile)
            funcs.run("titandb",dbfilename,workload,resultfile)
    
        if phase=="both":
            resultfile1 = resultfile+"_load"
            funcs.load("titandb",dbfilename,workload,resultfile1)
            resultfile2 = resultfile+"_run"
            funcs.run("titandb",dbfilename,workload,resultfile2)
    

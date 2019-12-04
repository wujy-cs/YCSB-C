import funcs
import sys
import os

dbPath = "/mnt/titan/"
valueSizes = ["20scan","100scan","1000scan","10000scan"]
#valueSizes = ["8KB"]
smallThresh = 1
midThresh = 30000
for valueSize in valueSizes:
    dbSize = "100GB"
    dbfilename = dbPath+"titandb_original"+"1KB"+dbSize
    workload = "./workloads/workload"+valueSize+dbSize+".spec"
    memtable = 64
    sepBeforeFlush = "true"
    threads = 8
    resultfile = "./resultDir/titandb"+valueSize+dbSize+"memtable"+str(memtable)+"thread"+str(threads)
    if sepBeforeFlush == "true":
        resultfile = resultfile + "before"


    configs = {
        "bloomBits":"10",
        "seekCompaction":"false",
        "directIO":"false",
        "compression":"false",
        "noCompaction":"true",
        "blockCache":str(8*1024*1024),
        "memtable":str(memtable*1024*1024),
        "numThreads":str(threads),
        "tiered":"false",
        "levelMerge":"false",
        "rangeMerge":"false",
        "sepBeforeFlush":sepBeforeFlush,
        "smallThresh":str(smallThresh),
        "midThresh":str(midThresh),
    }

    phase = sys.argv[1]

    if __name__ == '__main__':
        os.system("sync && echo 3 > /proc/sys/vm/drop_caches")

        if phase=="load":
            configs["noCompaction"] = "false"
        
        #set configs
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
            resultfile = resultfile+"_run"
            print(resultfile)
            funcs.run("titandb",dbfilename,workload,resultfile)

        if phase=="both":
            resultfile1 = resultfile+"_both"
            funcs.both("titandb",dbfilename,workload,resultfile1)
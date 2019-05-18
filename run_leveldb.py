import funcs
import sys
import os

dbPath = "/mnt/rocksdb/"
#dbPath = "/mnt/HDD/"
#valueSizes = ["128B","256B","512B","1KB","2KB","3KB","4KB"]
valueSizes = ["ratio"]
dbSize = "100GB"
for valueSize in valueSizes:
    workload = "./workloads/workload"+valueSize+dbSize+".spec"
    memtable = 1024
    threads = 16
    smallThresh = 256
    midThresh = 4000
    gcRatio = 0.3
    dbfilename = dbPath+"leveldb_selective"+valueSize+dbSize+"small"+str(smallThresh)+"mid"+str(midThresh)
    resultfile = "./resultDir/leveldb_selective"+valueSize+dbSize+"memtable"+str(memtable)+"small"+str(smallThresh)+"mid"+str(midThresh)

    configs = {
        "bloomBits":"10",
        "seekCompaction":"false",
        "directIO":"false",
        "compression":"false",
        "blockCache":str(64*1024*1024),
        "memtable":str(memtable*1024*1024),
        "noCompaction":"true",
        "numThreads":str(threads),
        "smallThresh":str(smallThresh),
        "midThresh":str(midThresh),
        "gcRatio":str(gcRatio),
        "preheat":"false",
    }

    phase = sys.argv[1]

    os.system("sync && echo 3 > /proc/sys/vm/drop_caches")
    for cfg in configs:
        funcs.modifyConfig("./configDir/leveldb_config.ini","config",cfg,configs[cfg])

    if len(sys.argv) == 3:
        resultfile = sys.argv[2]

    if phase=="load": 
        resultfile = resultfile+"_load"
        funcs.load("leveldb",dbfilename,workload,resultfile)

    if phase=="run":
        resultfile = resultfile+"_run"
        print(resultfile)
        funcs.run("leveldb",dbfilename,workload,resultfile)

    if phase=="both":
        resultfile1 = resultfile+"_load"
        funcs.load("leveldb",dbfilename,workload,resultfile1)
        resultfile2 = resultfile+"_run"
        funcs.run("leveldb",dbfilename,workload,resultfile2)
        

# Yahoo! Cloud System Benchmark
# Workload A: Update heavy workload
#   Application example: Session store recording recent actions
#                        
#   Read/update ratio: 50/50
#   Default data size: 1 KB records (10 fields, 100 bytes each, plus key)
#   Request distribution: zipfian

#10GB 1KB value

recordcount=314572800
#recordcount=4194304
operationcount=40000000
workload=com.yahoo.ycsb.workloads.CoreWorkload

readallfields=true

readproportion=1.0
updateproportion=0
scanproportion=0
insertproportion=0

fieldlength=1000
requestdistribution=zipfian
scanlengthdistribution=constant
maxscanlength=1000

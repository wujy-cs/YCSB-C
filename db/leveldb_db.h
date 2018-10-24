//
// Created by wujy on 18-1-21.
//

#ifndef YCSB_C_LEVELDB_DB_H
#define YCSB_C_LEVELDB_DB_H

#include "pebblesdb/db.h"
#include "core/db.h"
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

using std::string;

namespace ycsbc {
    class LevelDB : public DB{
    public:
        LevelDB(const char *dbfilename);
        int Read(const std::string &table, const std::string &key,
                 const std::vector<std::string> *fields,
                 std::vector<KVPair> &result);

        int Scan(const std::string &table, const std::string &key,
                 int len, const std::vector<std::string> *fields,
                 std::vector<std::vector<KVPair>> &result);

        int Insert(const std::string &table, const std::string &key,
                   std::vector<KVPair> &values);

        int Update(const std::string &table, const std::string &key,
                   std::vector<KVPair> &values);


        int Delete(const std::string &table, const std::string &key);

        void printStats();

        ~LevelDB();

    private:
        leveldb::DB *db_;
        unsigned noResult;
    };

    class ConfigLevelDB {
    private:
        boost::property_tree::ptree pt_;
        int bloomBits_;
        bool seekCompaction_;
        bool compression_;
        bool directIO_;
        int vlogThreads_;
        int expThreads_;
        size_t blockCache_;
        string vlogFilename_;
        string vlogDir_;
        size_t expdbMem_;

    public:
        ConfigLevelDB(){
            boost::property_tree::ini_parser::read_ini("./configDir/leveldb_config.ini",pt_);
            bloomBits_=pt_.get<int>("config.bloomBits");
            seekCompaction_=pt_.get<bool>("config.seekCompaction");
            compression_=pt_.get<bool>("config.compression");
            directIO_=pt_.get<bool>("config.directIO");
            blockCache_=pt_.get<size_t>("config.blockCache");
            vlogFilename_=pt_.get<string>("vlog.vlogFilename");
            vlogDir_=pt_.get<string>("expdb.vlogDir");
            vlogThreads_=pt_.get<int>("vlog.scanThreads");
            expThreads_=pt_.get<int>("expdb.expThreads");
            expdbMem_=pt_.get<size_t>("expdb.memSize");
        }

        int getBloomBits(){
            return bloomBits_;
        }

        bool getSeekCompaction(){
            return seekCompaction_;
        }

        bool getCompression(){
            return compression_;
        }

        bool getDirectIO(){
            return directIO_;
        }

        int getVlogThreads(){
            return vlogThreads_;
        }

        string getVlogFilename(){
            return vlogFilename_;
        }

        string getVlogDir(){
            return vlogDir_;
        }

        int getExpThreads(){
            return expThreads_;
        }

        size_t getBlockCache(){
            return blockCache_;
        }

        size_t getExpdbMem(){
            return expdbMem_;
        }
    };
}

#endif //YCSB_C_LEVELDB_DB_H

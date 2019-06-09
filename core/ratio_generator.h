//
// Created by wujy on 5/14/19.
//

#ifndef YCSB_C_RATIOGENERATOR_H
#define YCSB_C_RATIOGENERATOR_H

#include "generator.h"
#include <random>

namespace ycsbc {

    class RatioGenerator : public Generator<uint64_t> {
    public:
        RatioGenerator(double smallratio, double midratio, double largeratio):dists_(3){
            dists_[0] = std::uniform_int_distribution<uint64_t>(1,64);
            dists_[1] = std::uniform_int_distribution<uint64_t>(65,1024);
            dists_[2] = std::uniform_int_distribution<uint64_t>(1025,8192);
            d_.AddValue(1,smallratio);
            d_.AddValue(2,midratio);
            d_.AddValue(3,largeratio);
            Next();
        }
        uint64_t Next() {
            int choosen = d_.Next();
            switch (choosen) {
                case 1:
                    return last_int_ = dists_[0](generator_);
                case 2:
                    return last_int_ = dists_[1](generator_);
                case 3:
                    return last_int_ = dists_[2](generator_);
                default:
                    return last_int_ = dists_[1](generator_);
            }
        }

        uint64_t Last() { return last_int_; }

    private:
        uint64_t last_int_;
        std::mt19937_64 generator_;
        std::vector<std::uniform_int_distribution<uint64_t>> dists_;
        DiscreteGenerator<int> d_;
    };

} // ycsbc

#endif //YCSB_C_RATIOGENERATOR_H
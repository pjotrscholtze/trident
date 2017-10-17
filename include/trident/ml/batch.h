#ifndef BATCH_H_
#define BATCH_H_

#include <trident/ml/feedback.h>
#include <trident/utils/memoryfile.h>

#include <string>
#include <vector>
#include <random>

using namespace std;

class BatchCreator {
    private:
        const string kbdir;
        const uint64_t batchsize;
        const uint16_t nthreads;
        const float valid;
        const float test;
        const bool createBatchFile;

        const bool filter;
        const std::shared_ptr<Feedback> feedback;

        std::unique_ptr<MemoryMappedFile> mappedFile;
        const char* rawtriples;
        uint64_t ntriples;
        std::vector<uint64_t> indices;
        uint64_t currentidx;
        std::default_random_engine engine;

        bool shouldBeUsed(long s, long p, long o);

        void createInputForBatch(bool createTraining,
                const float valid,
                const float test);

    public:
        BatchCreator(string kbdir, uint64_t batchsize, uint16_t nthreads,
                const float valid, const float test, const bool filter,
                const bool createBatchFile,
                shared_ptr<Feedback> feedback);

        BatchCreator(string kbdir, uint64_t batchsize, uint16_t nthreads) :
            BatchCreator(kbdir, batchsize, nthreads, 0, 0, false, true,
                    std::shared_ptr<Feedback>()) {
            }

        void start();

        bool getBatch(std::vector<uint64_t> &output);

        bool getBatch(std::vector<uint64_t> &output1,
                std::vector<uint64_t> &output2,
                std::vector<uint64_t> &output3);

        string getValidPath();

        string getTestPath();

        std::shared_ptr<Feedback> getFeedback();

        static string getValidPath(string kbdir);

        static string getTestPath(string kbdir);

        static void loadTriples(string path, std::vector<uint64_t> &output);
};

#endif

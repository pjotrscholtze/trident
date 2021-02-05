/*
 * Copyright 2017 Jacopo Urbani
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
**/


#ifndef _STATS_H
#define _STATS_H


class Stats {
private:
    int64_t readIndexBlocks;
    int64_t readIndexBytes;
public:

    Stats() : readIndexBlocks(0), readIndexBytes(0) {}

    void incrNReadIndexBlocks() {
        readIndexBlocks++;
    }

    void addNReadIndexBytes(const uint64_t bytes) {
        readIndexBytes += bytes;
    }

    uint64_t getNReadIndexBlocks() const {
        return readIndexBlocks;
    }

    uint64_t getNReadIndexBytes() const {
        return readIndexBytes;
    }
};

class QueryStats {
public:
    unsigned long hash;
    int relativeQueryNumber;
    int repetition;
    double queryopti;
    double queryexec;
    double totalexec;
    uint64_t nResultingRows;
    uint64_t indexCounter[6];
    bool finished;
    // struct Counters {
        int64_t statsRow;
        int64_t statsColumn;
        int64_t statsCluster;
        int64_t aggrIndices;
        int64_t notAggrIndices;
        int64_t cacheIndices;
        int64_t spo, ops, pos, sop, osp, pso;
    // };
    bool internalErrorPlanGenerationFailed;
    bool parseError;
    bool semanticError;
    bool emptyResultKnownEmpty;
};

#endif

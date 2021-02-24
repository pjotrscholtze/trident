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


#include <trident/tree/nodemanager.h>

#include <iostream>
#include <fstream>
#include <algorithm>

char one[1] = { 1 };
char zero[1] = { 0 };
NodeManagerStats stats = *(new NodeManagerStats());
void NodeManagerStats::increment(short index) {
    this->fileTouches[index]++;
}

NodeManagerStats NodeManager::getStats() {
    return stats;
}

unsigned int NodeManagerStats::getMaxIndex(){
    return NODE_MANAGER_FILE_ACCESS_STATS_SIZE;
}

NodeManager::NodeManager(TreeContext *context, int nodeMinBytes,
        int fileMaxSize, int maxNFiles, int64_t cacheMaxSize, std::string path) :
    readOnly(context->isReadOnly()), path(path), nodeMinSize(nodeMinBytes) {
        lastNodeInserted = NULL;

        //Init filemanager
        //Calculate the highest file
        lastCreatedFile = 0;
        if (Utils::exists(path) && Utils::isDirectory(path)) {
            auto children = Utils::getFiles(path);
            for (auto child : children) {
                if (!Utils::hasExtension(child)) {
                    short idx = (short) atoi(Utils::filename(child).c_str());
                    if (lastCreatedFile < idx)
                        lastCreatedFile = idx;
                }
            }
        }
        bytesTracker = new MemoryManager<FileDescriptor>(cacheMaxSize);
        this->manager = new FileManager<FileDescriptor, FileDescriptor>(path,
                context->isReadOnly(), fileMaxSize, maxNFiles, lastCreatedFile,
                bytesTracker, NULL);

        //Init storedNodes and firstElementPerFile
        string file = path + DIR_SEP + string("idx");

        if (!readOnly) {
            readOnlyStoredNodes = NULL;
            nodesLoaded = NULL;
            rawInput = NULL;

            //Load existing nodes in the array
            if (Utils::exists(file) && Utils::fileSize(file) > 0) {
                mappedFile = std::unique_ptr<MemoryMappedFile>(new MemoryMappedFile(file));
                rawInput = mappedFile->getData();

                int nNodes = Utils::decode_int(rawInput, 0);
                nodesLoaded = new bool[nNodes];
                memset(nodesLoaded, 0, nNodes * sizeof(bool));
                readOnlyStoredNodes = new CachedNode[nNodes];
            }

        } else {
            //Load the nodes in the array
            if (Utils::exists(file) && Utils::fileSize(file) > 0) {
                mappedFile = std::unique_ptr<MemoryMappedFile>(new MemoryMappedFile(file));
                rawInput = mappedFile->getData();

                int nNodes = Utils::decode_int(rawInput, 0);
                nodesLoaded = new bool[nNodes];
                memset(nodesLoaded, 0, nNodes * sizeof(bool));
                readOnlyStoredNodes = new CachedNode[nNodes];
            }
        }
    }

void NodeManager::unserializeNodeFrom(CachedNode *node, char *buffer, int pos) {
    int64_t id = Utils::decode_long(buffer, pos);
    pos += 8;

    bool canHaveChildren = buffer[pos++] == 1 ? true : false;
    short fileIndex = (short) Utils::decode_int(buffer, pos);
    pos += 4;
    int fileOffset = Utils::decode_int(buffer, pos);
    pos += 4;
    int nodeSize = Utils::decode_int(buffer, pos);
    pos += 4;
    int availableSize = Utils::decode_int(buffer, pos);

    node->id = id;
    node->nodeSize = nodeSize;
    node->children = canHaveChildren;
    node->fileIndex = fileIndex;
    node->posIndex = fileOffset;
    node->availableSize = availableSize;
}

int NodeManager::serializeTo(CachedNode *node, char *buffer) {
    int pos = 0;
    Utils::encode_long(buffer, pos, node->id);
    pos += 8;
    buffer[pos++] = node->children ? 1 : 0;
    Utils::encode_int(buffer, pos, node->fileIndex);
    pos += 4;
    Utils::encode_int(buffer, pos, node->posIndex);
    pos += 4;
    Utils::encode_int(buffer, pos, node->nodeSize);
    pos += 4;
    Utils::encode_int(buffer, pos, node->availableSize);
    pos += 4;
    return pos;
}

char* NodeManager::get(CachedNode *node) {
    // LOG(INFOL) << "NodeManager::get ~ node->id" << node->id;
    // LOG(INFOL) << "NodeManager" << node->fileIndex;
    // stats.fileTouches[node->fileIndex]++;
    stats.increment(node->fileIndex);
    uint64_t len = node->nodeSize;
    return manager->getBuffer(node->fileIndex, node->posIndex, &len);
}

CachedNode *NodeManager::getCachedNode(int64_t id) {
    if (readOnly) {
        if (!nodesLoaded[id]) {
            //Load the node from rawInput
            int pos = Utils::decode_int(rawInput, 4 + id * 4);
            unserializeNodeFrom(readOnlyStoredNodes + id, rawInput, pos);
            nodesLoaded[id] = true;
        }
        CachedNode *res = readOnlyStoredNodes + id;
        // NodeManager::fileAccesses[res->fileIndex]++;
        stats.increment(res->fileIndex);
        // LOG(INFOL) << "NodeManager" << res->fileIndex;
        return res;
    } else {
        auto itr = storedNodes.find(id);
        if (itr != storedNodes.end()) {
            stats.increment(itr->second->fileIndex);
            // NodeManager::fileAccesses[itr->second->fileIndex]++;
            // LOG(INFOL) << "NodeManager" << itr->second->fileIndex;
            return itr->second;
        } else {
            return NULL;
        }
    }
}

void NodeManager::put(Node *node, char *buffer, int sizeBuffer) {
    //First check if there is already a cachedNode existing
    CachedNode *cn = getCachedNode(node->getId());
    if (cn != NULL) {
        if (sizeBuffer > cn->availableSize) {
            LOG(DEBUGL) << "Node " << cn->id << " is " << (sizeBuffer - cn->availableSize) << "  bytes larger. Current size is " << cn->availableSize << " Must increase file " << cn->fileIndex;
            //int diff = sizeBuffer - cn->availableSize;
            int diff = (sizeBuffer - cn->availableSize + 1023) & ~1023;
            //Enlarge the file
            manager->shiftRemainingFile(cn->fileIndex, cn->posIndex, diff);
            // Update positions of all the nodes stored in the same file
            cn->availableSize += diff;
            CachedNode *next = cn->next;
            while (next != NULL) {
                next->posIndex += diff;
                next = next->next;
            }
        }

        //Replace the content and update the nodeSize
        uint64_t len = sizeBuffer;
        char *b = manager->getBuffer(cn->fileIndex, cn->posIndex, &len);
        memcpy(b, buffer, sizeBuffer);
        cn->nodeSize = sizeBuffer;
    } else {
        CachedNode *c = new CachedNode;
        //Fill all the fields
        c->id = node->getId();
        c->children = node->canHaveChildren();
        c->nodeSize = sizeBuffer;
        c->availableSize = std::max(nodeMinSize, sizeBuffer);

        //Is the file too big?
        if (manager->sizeLastFile() >= manager->getFileMaxSize()) {
            lastCreatedFile = manager->createNewFile();
            lastNodeInserted = NULL;
        }

        // Update the metadata
        c->fileIndex = lastCreatedFile;
        c->posIndex = manager->sizeFile(lastCreatedFile);
        c->previous = NULL;
        c->next = NULL;
        if (lastNodeInserted == NULL) {
            lastNodeInserted = c;
            // this node is the first in the file
            firstElementsPerFile.push_back(c);
        } else {
            c->previous = lastNodeInserted;
            lastNodeInserted->next = c;
            lastNodeInserted = c;
        }
        //Write to disk
        manager->append(buffer, c->availableSize);

        //Put the cached node in the list
        storedNodes.insert(std::make_pair(c->id, c));
    }
}

void NodeManager::compressSpace(string path) {
    //1-- Load all the nodes and sort them by file
    vector<vector<CachedNode> > nodes;
    string sFileIdx = path + DIR_SEP + string("idx");
    int totalNumberNodes = 0;
    if (Utils::exists(path) && Utils::fileSize(sFileIdx) > 0) {
        MemoryMappedFile mf(sFileIdx);
        int64_t size = mf.getLength();
        char *raw_input = mf.getData();
        
        int nnodes = Utils::decode_int(raw_input, 0);
        int64_t pos = 4 + 4 * nnodes;

        int currentFile = -1;
        while (pos < size) {
            bool isFirst = raw_input[pos++];
            CachedNode node;
            unserializeNodeFrom(&node, raw_input, pos);
            pos += NODE_SIZE;
            if (isFirst) {
                nodes.push_back(vector<CachedNode>());
                currentFile++;
            }
            nodes[currentFile].push_back(node);
            totalNumberNodes++;
        }
    }

    //2-- Rewrite each file eliminating the blank spaces
    char *supportBuffer = new char[SIZE_SUPPORT_BUFFER];
    Utils::remove(sFileIdx);
    ofstream fileIdx(sFileIdx, ios_base::binary);
    int sizeCoordinates = 4 * totalNumberNodes;
    char *coordinatesSpace = new char[sizeCoordinates];
    Utils::encode_int(coordinatesSpace, 0, totalNumberNodes);
    fileIdx.write(coordinatesSpace, 4);
    //Move the file to the next position
    fileIdx.seekp(4 + sizeCoordinates);

    for (int i = 0; i < nodes.size(); ++i) {
        vector<CachedNode> *fileNodes = &nodes[i];
        //Open the old file and create a new file
        string pOldFile = path + DIR_SEP + to_string(i);
        ifstream sOldfile(pOldFile, ios_base::binary);
        string pNewFile = path + DIR_SEP + to_string(i) + ".new";
        ofstream sNewFile(pNewFile, ios_base::binary);

        //Go through all the nodes and copy the contents from the old node to the new one
        int size = fileNodes->size();
        bool first = true;
        for (int j = 0; j < size; ++j) {
            CachedNode *node = &((*fileNodes)[j]);
            //Move to the correct location
            sOldfile.seekg(node->posIndex);
            node->posIndex = sNewFile.tellp();
            sOldfile.read(supportBuffer, node->nodeSize);
            sNewFile.write(supportBuffer, node->nodeSize);
            node->availableSize = node->nodeSize;

            if (first) {
                fileIdx.write(one, 1);
                first = false;
            } else {
                fileIdx.write(zero, 1);
            }
            int p = serializeTo(node, supportBuffer);
            Utils::encode_int(coordinatesSpace, node->id * 4, fileIdx.tellp());
            fileIdx.write(supportBuffer, p);
        }
        sOldfile.close();
        sNewFile.close();

        //Remove the old file
        int64_t oldSize = Utils::fileSize(pOldFile);
        Utils::remove_all(pOldFile);

        //Rename the new file
        int64_t newSize = Utils::fileSize(pNewFile);
        Utils::rename(pNewFile, pOldFile);

        LOG(DEBUGL) << "Oldsize file " << i << ": " << oldSize << " newsize: " << newSize;
    }
    fileIdx.seekp(4);
    fileIdx.write(coordinatesSpace, sizeCoordinates);
    fileIdx.close();
    delete[] supportBuffer;
    delete[] coordinatesSpace;
}

NodeManager::~NodeManager() {

    delete bytesTracker;

    if (!readOnly) {
        string file = path + DIR_SEP + string("idx");
        ofstream out(file, ios_base::binary);
        char supportBuffer[512];

        //Write at the beginning of the file the number of nodes and the position where the nodes are being stored
        Utils::encode_int(supportBuffer, 0, storedNodes.size());
        out.write(supportBuffer, 4);

        //Reserve some space to write the positions where the nodes are being stored.
        int sizeCoordinates = 4 * storedNodes.size();
        char *coordinatesSpace = new char[sizeCoordinates];
        //Move the file to the next position
        out.seekp(4 + sizeCoordinates);

        int64_t wastedSpace = 0;
        for (int i = 0; i < firstElementsPerFile.size(); ++i) {
            CachedNode *node = firstElementsPerFile[i];
            if (node != NULL) {
                out.write(one, 1);
                int p = serializeTo(node, supportBuffer);
                Utils::encode_int(coordinatesSpace, node->id * 4, out.tellp());
                out.write(supportBuffer, p);
                wastedSpace += node->availableSize - node->nodeSize;
                node = node->next;
                while (node != NULL) {
                    out.write(zero, 1);
                    int p = serializeTo(node, supportBuffer);
                    Utils::encode_int(coordinatesSpace, node->id * 4,
                            out.tellp());
                    out.write(supportBuffer, p);
                    wastedSpace += node->availableSize - node->nodeSize;
                    node = node->next;
                }
            }
        }

        //Write the coordinatesSpace
        out.seekp(4);
        out.write(coordinatesSpace, sizeCoordinates);
        delete[] coordinatesSpace;

        LOG(DEBUGL) << "Wasted space to store the nodes: " << wastedSpace;
        out.close();

        //Clean the stored nodes
        for (auto itr = storedNodes.begin(); itr != storedNodes.end(); ++itr) {
            delete itr->second;
        }
        storedNodes.clear();
    } else {
        delete[] readOnlyStoredNodes;
        delete[] nodesLoaded;
        rawInput = NULL;
    }

    delete manager;
}

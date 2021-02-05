import subprocess
def clean_queries():
    with open("queries/queries_for_das.sparql.exclude", "r") as f:
        with open("queries/queries_all.sparql", "w") as f2:
            for line in f.readlines():
                if "construct" in line.lower(): continue
                f2.writelines([line])

def queries_into_chunks(chunk_size = 5000):
    with open("queries/queries_all.sparql", "r") as f:
        chunk_id = 0
        lines_in_chunk = 0
        chunk = []
        lines_raw = f.readlines()
        lines = list(set(lines_raw))
        print("lines_raw", len(lines_raw))
        print("lines", len(lines))
        for line in lines:
            chunk += [line]
            lines_in_chunk += 1
            if lines_in_chunk == chunk_size:
                yield (chunk_id, chunk)
                chunk = []
                lines_in_chunk = 0
                chunk_id += 1
        yield (chunk_id, chunk)

"""
    static unsigned long
    sdbm(str)
    unsigned char *str;
    {
        unsigned long hash = 0;
        int c;

        while (c = *str++)
            hash = c + (hash << 6) + (hash << 16) - hash;

        return hash;
    }
"""
def simple_hash(q):
    out = 0
    for i in range(0, len(q)):
        out = ord(q[i]) + ((out << 6) + (out << 16) - out)
    return out


def make_chunked_archives(chunk_size = 5000):
    for id, chunk in queries_into_chunks(chunk_size):
        with open("queries/query_chunk_%s.sparql" % id, "w") as f: 
            f.writelines(chunk)
    subprocess.run("tar -czf ./queries/chunked_queries.tar.gz ./queries/query_chunk_*.sparql", shell=True)
    subprocess.run("rm ./queries/query_chunk_*.sparql", shell=True)

make_chunked_archives(5000)

# total_lines = 0
# hashes = set()
# for id, chunk in queries_into_chunks(5000):
#     total_lines += len(chunk)
#     for line in chunk:
#         hashes.add(simple_hash(line))

# print(len(hashes), total_lines)
import json,urllib.parse,urllib.request,sys
Q=["Permutation Generation Methods Sedgewick","Ranking and unranking permutations in linear time","Enumerative source encoding Cover",
"A Block-sorting Lossless Data Compression Algorithm","Algorithm 235: Random permutation","Suffix arrays: a new method for on-line string searches",
"Trailing the dovetail shuffle to its lair","Shuffling cards and stopping times","Opportunistic data structures with applications",
"Permutations by interchanges Heap","Effective proximity retrieval by ordering permutations","Comparing top k lists",
"An algorithm for source coding Schalkwijk","Generation of permutations by adjacent transposition Trotter","Approximate similarity search in metric spaces using inverted files",
"Efficient generation of the binary reflected Gray code and its applications","Faster methods for random sampling Vitter","A new method for random permutations"]
for q in Q:
    u="https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per-page=3&select=title,cited_by_count,publication_year,doi,open_access,authorships&sort=relevance_score:desc"
    try: r=json.load(urllib.request.urlopen(u,timeout=20))["results"]
    except Exception as e: print(q,"ERR",e); continue
    print("##",q)
    for w in r[:2]:
        a=", ".join(x["author"]["display_name"] for x in w["authorships"][:3])
        print(f"  {w['cited_by_count']:>6}  {w['publication_year']}  {w['title'][:70]} | {a} | {w['doi']} | oa={w['open_access']['oa_url']}")

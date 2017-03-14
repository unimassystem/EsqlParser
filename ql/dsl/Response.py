'''
Created on Mar 10, 2017

@author: qs
'''

def parse_hit(cols,metas,hit):
    row = []
    for meta in metas:
        row.append(hit[meta])
    if '_source' not in hit:
        return row
    
    for col in cols:
        if col in hit['_source'].keys():
            row.append(hit['_source'][col])
        else:
            row.append(None)
    return row
    
    
def parse_hits_cols(hits):
    fields = {}
    for hit in hits:
        if '_source' in hit:
            for key in hit['_source'].keys():
                fields[key] = True
    return list(fields.keys())


def parse_hits(hits):
    
    if 'hits' not in hits:
        return
    hits = hits['hits']
    metas = ['_id','_index','_type']
    cols = parse_hits_cols(hits)
    rows = []
    for hit in hits:
        rows.append(parse_hit(cols,metas,hit))
    retval = {}
    retval['cols'] = metas + cols
    retval['rows'] = rows
    return retval


def parse_aggs_cols(aggs,bks):
    for k in aggs.keys():
        if type(aggs[k]) != dict:
            continue
        if 'buckets' in aggs[k].keys():
            bks.append(k)
            buckets = aggs[k]['buckets']
            if len(buckets) > 0:
                parse_aggs_cols(buckets[0],bks)
    


def parse_aggs_rows(aggs,bks,depth,rows,bucket_vals=[]):
    bucket_name = None
    if depth < len(bks):
        bucket_name = bks[depth]
        if 'buckets' in aggs[bucket_name] :
            for bucket in aggs[bucket_name]['buckets']:
                if 'key_as_string' in bucket:
                    bucket_vals.append(bucket['key_as_string'])
                elif 'key' in bucket:
                    bucket_vals.append(bucket['key'])
                else:
                    bucket_vals.append(None)
                parse_aggs_rows(bucket,bks,depth + 1,rows,bucket_vals)
            if len(bucket_vals) > 0:
                bucket_vals.pop(len(bucket_vals) - 1) 
    else:
        row =  bucket_vals[:]
        mts = {}
        for mertic in aggs.keys():
            if type(aggs[mertic]) == dict and 'value' in aggs[mertic].keys():
                mts[mertic] = aggs[mertic]['value']
        rows.append((row,mts))
        if len(bucket_vals) > 0:
            bucket_vals.pop(len(bucket_vals) - 1) 
    pass
            


def get_agg_rows(bks,rows):
    
    mertics = {}
    for (bucket,mts) in rows:
        for m in mts.keys():
            mertics[m] = True
    for m in mertics.keys():
        bks.append(m)
    retval = []
    for (bucket,mts) in rows:
        row = bucket 
        for m in mertics.keys():
            if m in mts.keys():
                row.append(mts[m])
            else:
                row.append(None) 
        retval.append(row)
    return retval


def parse_aggregations(aggs):
    bks = []
    depth = 0
    rows = []
    retval = {}
    parse_aggs_cols(aggs,bks)
    parse_aggs_rows(aggs,bks,depth,rows)
    row_sets = get_agg_rows(bks,rows)
    retval['cols'] = bks
    retval['rows'] = row_sets
    return retval


def response(res):
    if 'aggregations' in res.keys():
        return parse_aggregations(res['aggregations'])
    if 'hits' in res.keys():
        return parse_hits(res['hits'])
    pass




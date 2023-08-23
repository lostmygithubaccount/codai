import ibis

con = ibis.duckdb.connect("cache.ddb", read_only=True)



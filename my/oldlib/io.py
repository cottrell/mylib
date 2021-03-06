"""
Stuff to do with reading and writing.
"""
import gzip
import inspect
import re

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def write_df_to_arrow_rbf(df, path, preserve_index=False):
    """ record batch file writer """
    t = pa.Table.from_pandas(df, preserve_index=preserve_index)
    w = pa.RecordBatchFileWriter(path, t.schema)
    print(f'writing {df.shape[0]} rows to {path}')
    w.write(t)
    w.close()


def read_arrow_rbf_to_df(path):
    """ record batch file reader """
    r = pa.RecordBatchFileReader(path)
    print(f'reading {path}')
    t = r.read_all()
    return t.to_pandas()


def get_capped_line_count(filename, n=2):
    i = 0
    for x in _open(filename):
        i += 1
        if i >= n:
            break
    return i


def _open(filename, **kwargs):
    if filename.endswith(".gz"):
        return gzip.open(filename, **kwargs)
    else:
        return open(filename, **kwargs)


parquet_options = {"compression": "snappy"}


def append_to_parquet_table(dataframe, filepath=None, writer=None):
    """
    Example recipe:

        writer = None
        for chunk in chunks:
            writer = append_to_parquet_table(chunk, filepath=filename, writer=writer)

    See: https://stackoverflow.com/questions/47113813/using-pyarrow-how-do-you-append-to-parquet-file
    """
    assert (filepath is not None) or (writer is not None), "filepath and writer can not both be None"
    table = pa.Table.from_pandas(dataframe)
    if writer is None:
        writer = pq.ParquetWriter(filepath, table.schema)
    writer.write_table(table=table)
    # TODO: figure out how to preserve_index false on the append mode case
    # table = pa.Table.from_pandas(df, preserve_index=False)
    # pq.write_to_dataset(table, root_path=outfile, partition_cols=['product'], preserve_index=False)
    return writer

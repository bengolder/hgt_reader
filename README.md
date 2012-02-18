This is a tiny repository for a script to read NASA SRTM hgt files, to put the
data into 3d modeling programs.

Example:

    >>> import hgt_reader
    >>> file_path = '/Users/benjamin/projects/ActiveMatter/data/N31E034.hgt'
    >>> data = hgt_reader.read(file_path)
    >>> from pprint import pprint
    >>> pprint(data[-1][-5:])
    [(34.99666666666667, 31.996666666666666, 585),
     (34.997500000000002, 31.997499999999999, 587),
     (34.998333333333335, 31.998333333333335, 590),
     (34.999166666666667, 31.999166666666667, 594),
     (35.0, 32.0, 598)]

As you can see in the example above, `read()` is the primary function to be
used. Read take an optional `arc_seconds` argument that can be set to either `3` or `1`:

    def read(filePath, arc_seconds=3):



'''
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


'''
import struct
import os

def _hgt_size(arc_seconds):
    # if it is a worldwide file
    if arc_seconds == 3:
        return 1201
    # if it is a U.S. file
    elif arc_seconds == 1:
        return 3601
    else:
        print 'You must use either 1 or 3 arc seconds.'
        raise

def patch_holes(heights, holes, row_size):
    count = 0
    for x in holes:
        count += 1
        y = holes[x]
        neighbors = []
        if x > 0:
            neighbors.append(heights[x-1][y])
            if y > 0:
                neighbors.append(heights[x-1][y-1])
            if y < row_size - 1:
                neighbors.append(heights[x-1][y+1])
        if x < row_size - 1:
            neighbors.append(heights[x+1][y])
            if y > 0:
                neighbors.append(heights[x+1][y-1])
            if y < row_size - 1:
                neighbors.append(heights[x+1][y+1])
        if y > 0:
            neighbors.append(heights[x][y-1])
        if y < row_size - 1:
            neighbors.append(heights[x][y+1])
        valid_neighbors = [h for h in neighbors if h > -32600]
        if valid_neighbors:
            avg = sum(valid_neighbors) / len(valid_neighbors)
            heights[x][y] = avg
        else:
            print 'no valid neighbors for this hole!'
            return
    print '%s holes patched!' % count
    return heights

def frange(start, num_step, step):
    for i in range(num_step):
        yield start + i * step

def add_latlon(filePath, heights, row_size):
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    try:
        sgns = fileName[0], fileName[3]
        lat0, lon0 = float(fileName[1:3]), float(fileName[4:])
        if sgns[0] == 'S':
            lat0 *= -1
        if sgns[1] == 'W':
            lon0 *= -1
    except:
        print 'Incorrect File Name format for hgt file!'
        return
    step = 1.0/(row_size - 1)
    lats = [a for a in frange(lat0, row_size, step)]
    lats.reverse() # because the heights are read across, then top to bottom
    lons = [b for b in frange(lon0, row_size, step)]
    # build with a row per each lat, in descending order (top to bottom)
    # then a point in each lat row for each lon
    # switched to (lon, lat, z) because that is the (x, y, z)!
    new_rows = []
    for i, lat in enumerate(lats):
        new_row = []
        for j, lon in enumerate(lons):
            point = (lon, lat, heights[i][j])
            new_row.append(point)
        new_rows.append(new_row)
    return new_rows

def read(filePath, arc_seconds=3):
    number_format = '>h' # big-endian 16-bit signed integer
    f = open(filePath, 'rb')
    # 'row_length' being 1201 or 3601 and 'row' being the raw data for one row
    rows = []
    row_size = _hgt_size(arc_seconds)
    holes = {}
    for i in range(row_size): # for each row
        row = []
        for j in range(row_size):
            data = f.read(2) # read 16 bits/2 bytes
            # for some reason, it comes out as a tuple
            value = struct.unpack(number_format, data)[0]
            # keep track of cells without a valid height value
            if value < -3200:
                holes[i] = j
            row.append(value)
        rows.append(row)
    heights = patch_holes(rows, holes, row_size)
    points = add_latlon(filePath, heights, row_size)
    return points

def test(filePath):
    data = read(filePath)
    last = len(data) - 1
    print data[last][:5]
    print data[last][-5:]


if __name__=='__main__':
    path = '/Users/benjamin/projects/ActiveMatter/data/N31E034.hgt'
    test(path)








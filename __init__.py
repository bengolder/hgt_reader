'''
This is a tiny repository for a script to read NASA SRTM hgt files, to put the
data into 3d modeling programs.
'''
import struct

def _hgt_size(arc_seconds):
    # if it is a worldwide file
    if arc_seconds == 3:
        return 1201
    # if it is a U.S. file
    elif arc_seconds == 1:
        return 3601

def patch_holes(heights, holes, row_size):
    for x in holes:
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
            print 'replacing', heights[x][y],'with',avg
            heights[x][y] = avg
        else:
            print 'no valid neighbors for this hole!'
            return
    return heights

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
            if value == -32768:
                holes[i] = j
            row.append(value)
        rows.append(row)
    return patch_holes(rows, holes, row_size)

def test(filePath):
    data = read(filePath)
    for row in data[654:674]:
        pass
        #print 'sample =', row[-20:]
        #print 'average = %s' % (sum(row) / len(row))
        #print 'max = %s' % max(row)
        #print 'min = %s' % min(row)


if __name__=='__main__':
    path = '/Users/benjamin/projects/ActiveMatter/data/N31E034.hgt'
    test(path)








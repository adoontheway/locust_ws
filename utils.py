def check_sum(data):
    sum = 0
    idx = 0
    size = data.length
    for i in range(0,size/2):
        sum += data[idx:]
        idx += 2
    if size%2 != 0:
        sum += data[idx]
    return sum
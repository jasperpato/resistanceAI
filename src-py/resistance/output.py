import json
import random

if __name__=="__main__":
    data=None
    with open('genes.json') as f:
        data = json.load(f)["0"]
    for k in data.keys():
        print(f"{k}: {[round(data[k][0]*i*i+data[k][1]*i+data[k][2]*min(i,3)+data[k][3],3) for i in range(5)]}")
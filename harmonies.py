import collections
import pprint
import bisect

data = {}
primesa = []
primesb = []
primesc = []
with open("tokens.txt") as fi:
    for x in fi:
        p = x.strip().split(" ")
        cnt = int(p[0])
        name = p[1]
        data[name]=cnt
limit = len(data)
primes = []
with open("primes.0000") as fi:
    count = 0
    suma = 1
    sumb = 0
    for x in fi:
        count = count+1
        p = int(x.strip())
        primes.append(p)
        primesa.append(count)

count = 0
suma = 1
sumb = 0        
for x in primes[0:10]:
    count = count+1
    p = x
    suma = suma * p
    sumb = sumb + p
    primesb.append(sumb)
    primesc.append(suma)


primorials = [2, 6, 30, 210, 2310, 30030, 510510]

def find_primorial(value):
    index = bisect.bisect_left(primorials, value)
    if index == len(primorials):
        return None  # Value is larger than all primorials
    return primorials[index]



#print(f"The primorial for value {value} is {primorial}")

# now scan up to find the first
words =[]
words2 =[]
words_level =[]
layer_count = collections.Counter()
for x in collections.Counter(data).most_common():
    #print(x[0],"\t",x[1])
    words.append(x[0])
    words2.append(x[1])

    pp = find_primorial(x[1])
    words_level.append(pp)
    layer_count[pp] += 1

pprint.pprint({
    "layers":layer_count,
    "primes":primesa,
    "primesb":primesb,
    "primesc":primesc,
    "primes" : list(zip(range(len(words)),
                        primes,
                        #primesb,
                        #primesc,
                        words,
                        words2,words_level)),
    #"index": index,
})



 'primesc': [2,
             6,
             30,                    510510: 31}),
             210,                     30030: 562,
             2310,                     2310: 3600,
                                        210: 8266,
                                        6: 17337,
                                        2: 17225,
                                        30: 13570,
             30030,                     
             510510,
             9699690,
             223092870,
             6469693230]}

 {'layers': Counter(



 

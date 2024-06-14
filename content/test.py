import request as r

f = r.headers_generator()
while True:
    print(f.__next__())
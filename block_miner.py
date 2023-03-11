import time

while True:
    blocknumber = int(open('db/blocknumber.db', 'r').read())
    new_blocknumber = blocknumber + 1
    open('db/blocknumber.db', 'w').write(str(new_blocknumber))
    print(str(new_blocknumber))
    time.sleep(5)
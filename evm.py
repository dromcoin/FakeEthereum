import random
from dataclasses import asdict
from decoder import decode_raw_tx

def Block():
    blocknumber = int(open(f'db/blocknumber.db', 'r').read())
    return {"id": "PyEVM", "jsonrpc": "2.0", "result": str(hex(blocknumber))}

def nonce():
    nonce = random.randint(1000212121, 900001121210)
    return {"id": "PyEVM", "jsonrpc": "2.0", "result": str(hex(nonce))}

def getBalance(address):
    try:
        balance = int(open(f'db/addresses/{address}.db', 'r').read())
        return {"id": "PyEVM", "jsonrpc": "2.0", "result": str(hex(balance))}
    except Exception:
        return {"id": "PyEVM", "jsonrpc": "2.0", "result": "0x0"}
        pass


def Transaction(raw_tx):
    res = decode_raw_tx(raw_tx)
    hash_tx = asdict(res)["hash_tx"]
    claimed = open('db/claimed_tx.db', 'r').read()
    sender = str(asdict(res)["from_"]).lower()
    recipient = str(asdict(res)["to"]).lower()
    value = int(asdict(res)["value"])
    tx_nonce = asdict(res)["nonce"]
    if sender == recipient:
        return {'code': -32000, 'message': 'transaction not submitted'}
    else:
        if int(tx_nonce) < 1000212121:
            return {'code': -32000, 'message': 'transaction not submitted'}
        else:
            if hash_tx in claimed:
                return {'code': -32000, 'message': 'transaction not submitted'}
            else:
                try:
                    sender_balance = int(open(f'db/addresses/{sender}.db', 'r').read())
                    try:
                        recipient_balance = int(open(f'db/addresses/{recipient}.db', 'r').read())
                    except Exception:
                        open(f'db/addresses/{recipient}.db', 'w').write("0")
                        recipient_balance = 0
                    if sender_balance > value:
                        new_sender_balance = sender_balance - value
                        new_recipient_balance = recipient_balance + value
                        open(f'db/addresses/{sender}.db', 'w').write(str(new_sender_balance))
                        open(f'db/addresses/{recipient}.db', 'w').write(str(new_recipient_balance))
                        open('db/claimed_tx.db', 'a').write(f'{hash_tx}\n')
                        return {'code': 202, 'message': 'transaction submitted'}
                except Exception as e:
                    return e
                    pass

def getTransactionReceipt(tr_hash):
    return {"id":"pyevm","jsonrpc":"2.0","result":{"blockHash":"0x0","blockNumber":"0x0","contractAddress":"null","cumulativeGasUsed":"0x0","effectiveGasPrice":"0x0","from":"0x0","gasUsed":"0x0","logs":[{"address":"0x0","blockHash":"0x0","blockNumber":"0x0","data":"0x0","logIndex":"0x0","removed":"false","topics":["0x0","0x0","0x0","0x0"],"transactionHash": tr_hash,"transactionIndex":"0x0"}],"logsBloom":"0x0","status":"0x0","to":"0x0","transactionHash": tr_hash,"transactionIndex":"0x0"}}

def ethcall():
    return {"id":"PyEVM", "jsonrpc": "2.0","result": "0x0000000000000000000000000000000000000000000000000000000000000006"}
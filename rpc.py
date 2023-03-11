from flask import Flask, request, Response, json
from evm import Transaction, getBalance, Block, getTransactionReceipt, nonce, ethcall


app = Flask(__name__)


CHAIN_ID = 878787
sample_block = json.loads(open('db/sample_block.json', 'r').read())

# RPC API

@app.route("/", methods=['POST', 'OPTIONS'])
def rpc_metamask():
    if request.method == 'OPTIONS':
        resp = Response("")
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Max-Age'] = 600
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    if request.method == 'POST':
        req = request.json
        method = req["method"]
        if method == 'eth_chainId':
            resp = Response(json.dumps({"id": "PyEVM", "jsonrpc": "2.0", "result": str(hex(CHAIN_ID))}))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'net_version':
            resp = Response(json.dumps({"id": "PyEVM", "jsonrpc": "2.0", "result": str(CHAIN_ID)}))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_blockNumber':
            resp = Response(json.dumps(Block()))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_getBalance':
            address = req["params"][0].lower()
            resp = Response(json.dumps(getBalance(address)))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_estimateGas':
            resp = Response(json.dumps({"id": "PyEVM", "jsonrpc": "2.0", "result": "0x5208"}))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_gasPrice':
            resp = Response(json.dumps({"id": "PyEVM", "jsonrpc": "2.0", "result": "0x1000000"}))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_getCode':
            resp = Response(json.dumps({"id": "PyEVM", "jsonrpc": "2.0", "result": "0x0"}))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_getTransactionCount':
            resp = Response(json.dumps(nonce()))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_sendRawTransaction':
            raw_tx = req["params"][0]
            resp = Response(json.dumps(Transaction(raw_tx)))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_getTransactionReceipt':
            tr_hash = req["params"][0]
            resp = Response(json.dumps(getTransactionReceipt(tr_hash)))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_getBlockByNumber':
            resp = Response(json.dumps(sample_block))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        if method == 'eth_call':
            resp = Response(json.dumps(ethcall()))
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return resp
        resp = Response("")
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

# Plugins:
# to be continued

if __name__ == "__main__":
    app.run(port="1234", debug=True)
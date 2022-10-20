"""
MIT License

Copyright (c) 2021 **Author**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The Python implementation of Shamir's Secret Sharing used in this program is
available in the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0

The unmodified code is available here: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing


The purpose of this program is to simulate a system that relaibly confirms the total
of an entity's receivables by distributing the information about each 
debtor's balance amongst the other debtors using Shamir's [1979]secret sharing and 
aggregating this information on a blockchain.

"""

# python 3.9.6
# Ganache CLI v6.10.2 (ganache-core: 2.11.3)

from __future__ import division
from __future__ import print_function
import functools
import random
import csv
from web3 import Web3
import json
import time

# use same random numbers to create debtor's balances every run
random.seed(31)

# Connect to blockchain
# Make sure ganache is running
# $ ganache-cli --accounts 51 (num_recievables + 1 for owner account)

print('Python Client initializing ...')
# Wait for ganache to initialize
time.sleep(30)


# Uncomment next line if running in Docker compose
ganache_url = 'HTTP://receivablessum-ganache-1:8545'
# Uncomment next line if running ganache locally
# ganache_url = 'HTTP://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

# network description
num_receivables = 50
num_shares = 20
min_num_shares = 10

# 12th Mersenne Prime
# (for this application of Shamir [1979] we want a known prime number as close as
# possible to our security level; e.g.  desired security level of 128
# bits -- too large and all the ciphertext is large; too small and
# security is compromised)
_PRIME = 2 ** 127 - 1

_RINT = functools.partial(random.SystemRandom().randint, 0)


def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below. Returns y value of point on poly.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def make_random_shares(secret, minimum, shares, prime=_PRIME):
    """
    Generates a random shamir pool, returns the share
    points as a list of tuples.
    """
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    poly = [_RINT(prime - 1) for i in range(1, minimum)]
    poly[0] = secret  # set constant to secret
    # Pick (1,2,3...) as x values for points.
    # Evaluate the polynomial at each one of these points.
    points = [(i, _eval_at(poly, i, prime))
              for i in range(1, shares + 1)]
    return points


def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"

    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares, prime=_PRIME):
    """
    Recover the secret from share points
    (x, y points on the polynomial). Retrun the secret - intercept of the 
    polynomial.
    """
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)


def initialize_blockchain(_name, _date, _bal, _prime, _shares, _min_shares):
    """ Initialize blockchain and load descriptive data
        Return smart contract object and contract address """

    if web3.isConnected() == True:
        print('Connected to Blockchain at', ganache_url)
    else:
        print('Not connected to Blockchain')
        exit()

    # Set first Ethereum account as sender ('owner')
    web3.eth.defaultAccount = web3.eth.accounts[0]

    # Get bytecode - taken from compiler in Remix
    bytecode = '0x608060405234801561001057600080fd5b5033600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060008060030160046101000a81548163ffffffff021916908363ffffffff160217905550611067806100856000396000f300608060405260043610610083576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632de41bd9146100885780635c74d7ed146100e35780637284e4161461014957806380d5010c146102cb578063832ef39414610331578063c2f055da14610379578063fe48e55214610462575b600080fd5b34801561009457600080fd5b506100c9600480360381019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506104c8565b604051808215151515815260200191505060405180910390f35b3480156100ef57600080fd5b50610124600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610521565b6040518083151515158152602001821515151581526020019250505060405180910390f35b34801561015557600080fd5b5061015e61055f565b604051808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200180602001806020018863ffffffff1663ffffffff1681526020018763ffffffff1663ffffffff1681526020018681526020018563ffffffff1663ffffffff1681526020018463ffffffff1663ffffffff16815260200183810383528a818151815260200191508051906020019080838360005b83811015610222578082015181840152602081019050610207565b50505050905090810190601f16801561024f5780820380516001836020036101000a031916815260200191505b50838103825289818151815260200191508051906020019080838360005b8381101561028857808201518184015260208101905061026d565b50505050905090810190601f1680156102b55780820380516001836020036101000a031916815260200191505b509a505050505050505050505060405180910390f35b3480156102d757600080fd5b5061032f60048036038101908080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290505050610725565b005b34801561033d57600080fd5b5061035c60048036038101908080359060200190929190505050610c84565b604051808381526020018281526020019250505060405180910390f35b34801561038557600080fd5b50610460600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803563ffffffff16906020019092919080359060200190929190803563ffffffff169060200190929190803563ffffffff169060200190929190505050610ca8565b005b34801561046e57600080fd5b506104c660048036038101908080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290505050610e1b565b005b6000600760008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160009054906101000a900460ff169050919050565b60076020528060005260406000206000915090508060000160009054906101000a900460ff16908060000160019054906101000a900460ff16905082565b60008060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690806001018054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561061f5780601f106105f45761010080835404028352916020019161061f565b820191906000526020600020905b81548152906001019060200180831161060257829003601f168201915b505050505090806002018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156106bd5780601f10610692576101008083540402835291602001916106bd565b820191906000526020600020905b8154815290600101906020018083116106a057829003601f168201915b5050505050908060030160009054906101000a900463ffffffff16908060030160049054906101000a900463ffffffff16908060040154908060050160009054906101000a900463ffffffff16908060050160049054906101000a900463ffffffff16905088565b61072d610f7c565b600060011515600760003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160009054906101000a900460ff1615151415156107fa576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601a8152602001807f53656e646572206973206e6f7420612072656365697661626c6500000000000081525060200191505060405180910390fd5b6001600760003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160016101000a81548160ff021916908315150217905515156108ee576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f52656365697661626c652068617320616c72656164792075706c6f616465642081526020017f736861726573000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b6002600060050160009054906101000a900463ffffffff1663ffffffff16101515156109a8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260298152602001807f436f6e7472616374206465736372697074696f6e2064617461206973206e6f7481526020017f20636f6d706c657465000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b6000600384518115156109b757fe5b06141515610a53576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252603b8152602001807f536861726573206172726179206973206e6f74206d616465207570206f66206181526020017f206d756c7469706c65206f6620746872656520656c656d656e7473000000000081525060400191505060405180910390fd5b600090505b8251811015610c2457600060050160009054906101000a900463ffffffff1663ffffffff168382815181101515610a8b57fe5b9060200190602002015111151515610b31576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260338152602001807f5368617265207820706f696e74206973206772656174686572207468656e207481526020017f6865206e756d626572206f66207368617265730000000000000000000000000081525060400191505060405180910390fd5b8260018201815181101515610b4257fe5b90602001906020020151600860008584815181101515610b5e57fe5b90602001906020020151815260200190815260200160002060000154018260000181815250508260028201815181101515610b9557fe5b90602001906020020151600860008584815181101515610bb157fe5b906020019060200201518152602001908152602001600020600101540182602001818152505081600860008584815181101515610bea57fe5b9060200190602002015181526020019081526020016000206000820151816000015560208201518160010155905050600381019050610a58565b6001600760003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160016101000a81548160ff021916908315150217905550505050565b60086020528060005260406000206000915090508060000154908060010154905082565b600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610d0457600080fd5b600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166000800160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508560006001019080519060200190610d82929190610f96565b508460006002019080519060200190610d9c929190610f96565b5083600060030160006101000a81548163ffffffff021916908363ffffffff1602179055508260006004018190555081600060050160006101000a81548163ffffffff021916908363ffffffff16021790555080600060050160046101000a81548163ffffffff021916908363ffffffff160217905550505050505050565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610e7957600080fd5b600090505b8151811015610f78576001600760008484815181101515610e9b57fe5b9060200190602002015173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160006101000a81548160ff0219169083151502179055506000600760008484815181101515610f0d57fe5b9060200190602002015173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160016101000a81548160ff0219169083151502179055508080600101915050610e7e565b5050565b604080519081016040528060008152602001600081525090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10610fd757805160ff1916838001178555611005565b82800160010185558215611005579182015b82811115611004578251825591602001919060010190610fe9565b5b5090506110129190611016565b5090565b61103891905b8082111561103457600081600090555060010161101c565b5090565b905600a165627a7a723058207f15a50a2002579c81ce89b63198c2b60fce884b341a030749b3892ff7ca86190029'

    # Get abi - taken from comiler in Remix
    abi = json.loads('[{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"checkReceivable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"receivables_mapping","outputs":[{"name":"exists","type":"bool"},{"name":"uploaded_shares","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"description","outputs":[{"name":"owner","type":"address"},{"name":"name","type":"string"},{"name":"date","type":"string"},{"name":"assert_balance","type":"uint32"},{"name":"sum_balance","type":"uint32"},{"name":"prime","type":"uint256"},{"name":"shares","type":"uint32"},{"name":"min_shares","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_shares","type":"uint256[]"}],"name":"upLoadShares","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"cum_points","outputs":[{"name":"y","type":"uint256"},{"name":"number","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"},{"name":"_date","type":"string"},{"name":"_assert_balance","type":"uint32"},{"name":"_prime","type":"uint256"},{"name":"_shares","type":"uint32"},{"name":"_min_shares","type":"uint32"}],"name":"setDescription","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addresses","type":"address[]"}],"name":"setReceivables","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
    receivablessumContract = web3.eth.contract(abi=abi, bytecode=bytecode)

    # Submit the transaction that deploys the contract
    tx_hash = receivablessumContract.constructor().transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    # Assign the deployed smart contract to the rec_sum contract object and save the contract address
    rec_sum = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    contract_address = tx_receipt.contractAddress
    print('Contract is deployed and is at address:', tx_receipt.contractAddress)

    # Load the inital date onto the smart contract
    tx_hash = rec_sum.functions.setDescription(
        _name, _date, _bal, _prime, _shares, _min_shares).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print('Contract description has been loaded')

    # Load receivables addresses into the smart contract.
    tx_hash = rec_sum.functions.setReceivables(
        web3.eth.accounts[1:]).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print('Debtors addresses have been uploaded to the blockchain')

    # Return the contract object and the contract address
    return rec_sum, contract_address


def create_network(n):
    """ Create a random network of debtors for a entity 
        Return a list of n debtor's balances"""
    if n < 10:
        raise ValueError("need at least 10 customers")
    # generate a list of customer balances
    bal = list(random.sample(range(1000, 1000000), n))
    return bal


def share_balances(bal_ls, m, s):
    """Create shares of each debtors balance and distribute to m other debtors
     who are randomly chosen
     Return a list of distributed shares"""
    # Create a list of n empty lists to hold the shares. Shares will be in the same
    # order as bal_ls
    no_balances = len(bal_ls)

    distributed_shares = [[] for _ in range(no_balances)]
    # go though balances and distribute shares to random other customers.
    # print(distributed_shares)

    print('')
    print('Distributing shares to other debtors')
    for count, bal in enumerate(bal_ls):
        shares_ls = make_random_shares(bal, minimum=m, shares=s)
        # pick a share for the owner to keep
        share_to_keep = random.randint(0, s-1)
        # distribute a random share back to owner
        distributed_shares[count].append(shares_ls[share_to_keep])
        del shares_ls[share_to_keep]
        # pick a sample of other balances withoout duplicates and the ownwer of the shares
        pickable = list(range(no_balances))
        pickable.remove(count)  # take out owner from pickable list
        sample = random.sample(pickable, s-1)
        print('\rCompany ID', count, 'will distribute shares to',
              sample, '            ', end='')
        for share_no, bal_no in enumerate(sample):
            distributed_shares[bal_no].append(shares_ls[share_no])
            # distribute share_no+1 as share_no 0 kept by owner
    print('')
    return distributed_shares


def main():

    # create a random network of cutomers balances in a list
    bal_list = create_network(num_receivables)
    bal_total = sum(bal_list)
    print('Secret (sum of balances):                                                     ',
          bal_total)

    # Iniatilize Blockcahin and smart contract
    rec_sum, contract_address = initialize_blockchain(
        "Acme Corp", "31.12.19", bal_total, _PRIME, num_shares, min_num_shares)

    # Generate Shamir [1979] shares of each debtor's balance and distribute
    # shares to a randome slection of other debtors while keeping one share for
    # themselves.
    all_shares = share_balances(bal_list, 10, 20)

    # Prepare data for upload to blockchain by summing the y values of shares where 2
    # or more shares from the same x point have been recieved by a debtor.
    # also count the number of shares

    shares_flatten_list = []

    for shares in all_shares:
        shares_flatten_dict = {}
        for (x, y) in shares:
            if x in shares_flatten_dict.keys():
                # return the value for that key or return default 0 (and create key)
                shares_flatten_dict[x]['y'] = shares_flatten_dict.get(
                    x, {}).get('y', 0) + y
                # return the value for that key or return default 0 (and create key)
                shares_flatten_dict[x]['num'] = shares_flatten_dict.get(
                    x, {}).get('num', 0) + 1
            else:
                shares_flatten_dict[x] = {'y': y, 'num':  1}

        shares_flatten_list.append([[x, y['y'], y['num']]
                                   for (x, y) in shares_flatten_dict.items()])

    print('')
    print("Aggregating shares for each debtor")
    shares_flat_list = []
    for id, shares in enumerate(shares_flatten_list):
        # for each companies shares flatten the lists for upload
        shares_flat_list.append(
            [item for sublist in shares for item in sublist])
        print('\rAggregating shares for ID', id, end='')
    print("")

    # Upload the aggregated shares to the blockchain.
    print("")
    print("Uploading shares to the blockchain")
    for id, shares in enumerate(shares_flat_list):
        # Set debtors Ethereum account as sender
        web3.eth.defaultAccount = web3.eth.accounts[id+1]
        # construct transaction and send to blockchain
        tx_hash = rec_sum.functions.upLoadShares(shares).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        print('\rShares for ID', id, 'have been uploaded to the Blockchain', end='')
    print("")

    # Download the fully aggregated shares (from all debtors) from the blockchain.
    print("")
    print("Downloading shares from the blockchain")
    shares_down = []
    for id in range(1, num_shares+1):
        # Send message to blockchain to retrieve aggregate shares
        share = [id, rec_sum.functions.cum_points(id).call()[0]]
        shares_down.append([id, rec_sum.functions.cum_points(id).call()[0]])
        #print('\rShares for ID',id,'have been uploaded to the Blockchain',end='')
    print("")
    print('Shares downloaded', shares_down)

    print('')
    secret_down = recover_secret(shares_down)
    print('Secret recovered from shares downloaded is', secret_down)
    if bal_total == secret_down:
        print('Sume of receivabales =', bal_total, 'is equal to ', secret_down)
        print('\033[92mTest Suceeded\033[0m')
        print('')
    else:
        print('Sume of receivabales =', bal_total,
              'is not equal to ', secret_down)
        print('\033[91mTest Failed\033[0m')
        print('')

    min_list = random.sample(shares_down, min_num_shares)

    print('Secret recovered from minimum number of shares',
          recover_secret(min_list))

    # Write out shares

    # Write the shares to a csv file for analysis
    with open("all_shares.csv", 'w') as f:
        # for shares in all_shares:
        fc = csv.writer(f, delimiter=',', lineterminator='\n')
        fc.writerows(all_shares)

    # Write the aggregated shares to a csv file for analysis
    with open("agg_shares.csv", 'w') as f:
        # for shares in all_shares:
        fc = csv.writer(f, delimiter=',', lineterminator='\n')
        fc.writerows(shares_flat_list)

    # Write the shares retrieved from the blockchain to a csv file for analysis
    with open("full_agg_shares.csv", 'w') as f:
        # for shares in all_shares:
        fc = csv.writer(f, delimiter=',', lineterminator='\n')
        fc.writerows(shares_down)


if __name__ == '__main__':
    main()

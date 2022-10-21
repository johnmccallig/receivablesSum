# receivablesSum

## Introduction

ReceivablesSum is a prototype of a system that allows the confirmation of accounting liabilities between an entity and the entities that owe it money.

Each debtor will divide their balance outstanding to the entity into shares, using Shamir (1979), and distributes those shares to the other debtors of the entity. These shares are then aggregated and uploaded to a blockchain. A smart contract aggregates the shares and the **total** balance can be reconstructed by Lagrange interpolating the resulting polynomial.

email john.mccallig@ucd.ie for a copy of the paper on which this software is based.

You can run the software as follows:

## On github.com using docker-compose

Go to the **Actions** menu in this repository. Select **run receivables_sum_test**. gighub will create an ubuntu VM and run the python client and test blockchain as containers within a docker-compose network. After a few minutes, output should be available through the Actions menu.

This option does not involved downlaoding any files or applications to your computer.

## Locally using docker-compose

Clone the repistory to a local directory. Install docker ([](https://www.docker.com/)) and docker-compose.

In a terminal, make sure you are in the cloned directory. Issue the following command

```% docker-compose up```

## Full local installation

The following software must be installed
python 3 (tested with 3.7.7)
node.js and npm (https://nodejs.org/en/download/)
ganache-cli (use npm to install - % npm install -g ganache-cli)

The [web3](https://web3py.readthedocs.io/en/v5/)python package is required in the python environment.

The solidity smart contract is compiled with [remix] (https://remix.ethereum.org/) solc version 0.4.26
The compiled ABI and bytecode is hard-coded into the python client.

Start ganache with n+1 accounts in a terminal window

```% ganache-cli --accounts 51```

In another window execute the python client code - typical run given below.

The example code is set to distribute shares to 20 debtors.

```% python Receivable_Sum_Client_Test.py```

## Sample run

```Secret (sum of balances): 20729562

Connected to Blockchain at HTTP://127.0.0.1:8545
Contract is deployed and is at address:
0xfb39d6e836ecB0d35967191985d920292a7EB85e

Contract description has been loaded
Debtors addresses have been uploaded to the blockchain

Distributing shares to other debtors
Company ID 49 will distribute shares to [37, 43, 8, 32, 28, 48, 16, 26, 38, 2,
   39, 1, 29, 35, 22, 34, 42, 3, 36]

Aggregating shares for each debtor
Aggregating shares for ID 49

Uploading shares to the blockchain
Shares for ID 49 have been uploaded to the Blockchain

Downloading shares from the blockchain 41
Shares downloaded [[1, 4224987540867684792164086679296759118378], [2,
   4110162129264888883018486186931925677135], [3,
   4373851240543150806268849699303518385119],
43 [4, 4639166087080075704949460133477578602728], [5,
   3521755932046131481455426206783499936913], [6,
   4148130378620106717169052427700799772644],
44 [7, 4185303943454416762589626408131893506627], [8,
   4209422284626747520749674761413121013907], [9,
   4312776863393567381417306020168097112403],
45 [10, 4661425560142733165239137074604528218747], [11,
   4492821222599234036348380034294370160687], [12,
   3615588788339866384768148791490958019789],
46 [13, 4223200225850743171698607693473272954037], [14,
   4582905140539651722535147860844045025794], [15,
   4279402553308169254024175168753514493305],
 [16, 3987076122042563433749629672313953174654], [17,
4397377766077569765898637196311574908179], [18,
4889388640851348101525191887065491583664],
 [19, 4277830634790084954678634928366458263660], [20,
4486363299531957286009502256909439950507]]

Secret recovered from shares downloaded is 20729562
Sum of receivables = 20729562 is equal to  20729562
Test Suceeded
Secret recovered from minimum number of shares 20729562
%
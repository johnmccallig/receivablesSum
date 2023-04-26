# receivablesSum

## Introduction

ReceivablesSum is a prototype of a system that allows the confirmation of accounting liabilities between an entity and the entities that owe it money.

Each debtor will divide their balance outstanding to the entity into shares, using Shamir (1979), and distribute those shares to the other debtors of the entity. These shares are then aggregated and uploaded to a blockchain. A smart contract aggregates the shares and the **total** balance can be reconstructed by Lagrange interpolating the resulting polynomial.

Email john.mccallig@ucd.ie for a copy of the paper on which this software is based.

You can run the software as follows:

## Locally using docker-compose

Clone the repository to a local directory.
```
% git clone https://github.com/johnmccallig/receivablesSum
```

Install [docker](https://www.docker.com/) and docker-compose.

In a terminal, make sure you are in the cloned directory. Issue the following command

```
% docker-compose up
```

When the application has terminated you will need to press ctrl-c or issue the following command in another terminal

```
% docker-compose down
```

## Full local installation

The following software must be installed
python 3 (tested with 3.9)
node.js and npm (https://nodejs.org/en/download/)
ganache-cli (use npm to install - % npm install -g ganache-cli)

The [web3](https://web3py.readthedocs.io/en/v5/) python package version 5.12.0 is required in the python environment.

The solidity smart contract is compiled with [remix](https://remix.ethereum.org/) solc version 0.4.26
The compiled ABI and bytecode is hard-coded into the python client.

Start ganache with n+1 accounts in a terminal window

```% ganache-cli --accounts 51```

In the python file Receivables_Sum_Client_Test.py make sure the ganache url is set to local.

```
# ganache_url = 'HTTP://receivablessum-ganache-1:8545'
# Uncomment next line if running ganache locally
ganache_url = 'HTTP://127.0.0.1:8545'
```

In another window execute the python client code - sample run given below.

The example code is set to distribute shares to 20 debtors.

```% python Receivable_Sum_Client_Test.py```

## Sample run

```Python Client initializing ...
266
Secret (sum of balances):                                                      20729562
267
Connected to Blockchain at HTTP://receivablessum-ganache-1:8545
268
Contract is deployed and is at address: 0x7a6563460949218d7f6F9e4183e3D49DFDB2B920
269
Contract description has been loaded
270
Debtors addresses have been uploaded to the blockchain
271

272
Distributing shares to other debtors
273

274
Company ID 0 will distribute shares to [4, 49, 12, 23, 9, 14, 10, 25, 2, 6, 34, 29, 44, 37, 28, 24, 13, 22, 21]             
275
Company ID 1 will distribute shares to [31, 3, 17, 22, 19, 46, 37, 26, 49, 21, 14, 7, 20, 12, 35, 45, 6, 36, 38]             
276
Company ID 2 will distribute shares to [39, 24, 45, 7, 43, 26, 19, 20, 13, 8, 30, 41, 22, 29, 44, 4, 40, 18, 34]             
277
Company ID 3 will distribute shares to [13, 49, 22, 11, 10, 31, 4, 32, 40, 33, 18, 24, 42, 2, 8, 37, 9, 34, 27]             
278
Company ID 4 will distribute shares to [17, 32, 31, 23, 16, 0, 7, 25, 38, 19, 29, 12, 2, 9, 8, 3, 14, 13, 47]             
279
Company ID 5 will distribute shares to [45, 12, 36, 30, 47, 33, 34, 44, 26, 15, 43, 13, 46, 20, 37, 21, 9, 24, 3]             
280
Company ID 6 will distribute shares to [23, 48, 13, 19, 45, 25, 38, 11, 2, 8, 28, 14, 10, 16, 44, 20, 43, 39, 29]             
281
Company ID 7 will distribute shares to [35, 38, 16, 18, 2, 45, 31, 40, 46, 17, 49, 13, 28, 24, 14, 26, 44, 29, 48]             
282
Company ID 8 will distribute shares to [16, 14, 21, 23, 20, 24, 7, 48, 4, 49, 31, 32, 29, 18, 12, 27, 2, 41, 40]             
283
Company ID 9 will distribute shares to [20, 31, 0, 47, 18, 25, 45, 19, 49, 16, 38, 41, 26, 15, 40, 10, 21, 6, 22]             
284
Company ID 10 will distribute shares to [46, 13, 1, 24, 35, 32, 20, 31, 34, 17, 43, 25, 26, 14, 15, 27, 3, 16, 42]             
285
Company ID 11 will distribute shares to [3, 27, 44, 21, 18, 6, 36, 49, 46, 16, 32, 28, 9, 42, 20, 41, 2, 48, 7]             
286
Company ID 12 will distribute shares to [29, 35, 9, 4, 1, 32, 31, 49, 18, 43, 40, 0, 22, 16, 10, 5, 30, 23, 45]             
287
Company ID 13 will distribute shares to [26, 21, 40, 25, 12, 27, 15, 3, 29, 2, 44, 41, 49, 8, 34, 48, 28, 16, 18]             
288
Company ID 14 will distribute shares to [5, 30, 3, 8, 38, 20, 12, 46, 25, 48, 15, 18, 22, 37, 27, 21, 45, 29, 35]             
289
Company ID 15 will distribute shares to [22, 4, 11, 42, 14, 17, 10, 7, 6, 20, 18, 29, 28, 12, 5, 33, 41, 49, 26]             
290
Company ID 16 will distribute shares to [32, 31, 23, 9, 45, 28, 48, 46, 3, 17, 39, 21, 38, 20, 41, 37, 7, 14, 18]             
291
Company ID 17 will distribute shares to [38, 49, 11, 16, 8, 35, 20, 25, 39, 29, 44, 21, 46, 4, 10, 9, 34, 31, 32]             
292
Company ID 18 will distribute shares to [47, 46, 9, 28, 30, 11, 44, 45, 33, 8, 38, 23, 25, 32, 12, 31, 22, 0, 15]             
293
Company ID 19 will distribute shares to [43, 12, 47, 8, 31, 20, 10, 13, 6, 30, 38, 32, 23, 46, 4, 18, 49, 35, 3]             
294
Company ID 20 will distribute shares to [3, 23, 37, 11, 15, 4, 24, 27, 42, 19, 34, 49, 40, 26, 6, 44, 35, 36, 5]             
295
Company ID 21 will distribute shares to [18, 10, 42, 2, 23, 4, 35, 9, 26, 49, 6, 20, 15, 37, 31, 45, 27, 28, 34]             
296
Company ID 22 will distribute shares to [16, 46, 0, 41, 36, 15, 13, 37, 1, 9, 39, 6, 17, 12, 32, 14, 23, 30, 5]             
297
Company ID 23 will distribute shares to [30, 45, 24, 14, 17, 42, 22, 48, 49, 21, 25, 12, 28, 27, 35, 2, 1, 41, 44]             
298
Company ID 24 will distribute shares to [34, 38, 31, 27, 5, 33, 39, 48, 30, 32, 36, 49, 43, 1, 0, 15, 44, 3, 12]             
299
Company ID 25 will distribute shares to [49, 26, 17, 5, 29, 15, 10, 45, 39, 44, 48, 11, 32, 14, 8, 47, 21, 2, 35]             
300
Company ID 26 will distribute shares to [45, 41, 6, 1, 25, 49, 2, 30, 36, 47, 29, 7, 33, 42, 24, 19, 10, 4, 37]             
301
Company ID 27 will distribute shares to [10, 39, 18, 23, 17, 8, 7, 9, 16, 37, 4, 48, 13, 32, 2, 19, 29, 40, 44]             
302
Company ID 28 will distribute shares to [46, 3, 37, 24, 34, 48, 2, 43, 47, 12, 9, 16, 7, 29, 5, 35, 4, 33, 26]             
303
Company ID 29 will distribute shares to [20, 24, 18, 49, 7, 23, 40, 3, 10, 27, 35, 32, 14, 31, 37, 34, 1, 42, 22]             
304
Company ID 30 will distribute shares to [22, 39, 34, 15, 40, 14, 9, 3, 29, 43, 37, 48, 7, 35, 25, 23, 5, 16, 46]             
305
Company ID 31 will distribute shares to [34, 18, 43, 36, 39, 25, 33, 22, 6, 24, 46, 3, 9, 23, 0, 37, 15, 7, 47]             
306
Company ID 32 will distribute shares to [48, 12, 44, 22, 38, 49, 21, 1, 16, 17, 25, 24, 18, 34, 23, 13, 20, 47, 2]             
307
Company ID 33 will distribute shares to [37, 20, 46, 42, 16, 35, 9, 15, 36, 29, 4, 2, 34, 19, 22, 32, 21, 45, 8]             
308
Company ID 34 will distribute shares to [32, 27, 38, 47, 0, 41, 39, 37, 13, 28, 42, 20, 4, 33, 19, 46, 23, 25, 30]             
309
Company ID 35 will distribute shares to [47, 25, 2, 45, 41, 0, 5, 39, 38, 19, 13, 26, 27, 30, 37, 20, 11, 6, 40]             
310
Company ID 36 will distribute shares to [14, 40, 5, 12, 24, 47, 27, 37, 33, 31, 17, 34, 10, 6, 38, 15, 43, 22, 13]             
311
Company ID 37 will distribute shares to [32, 17, 16, 11, 1, 20, 36, 6, 21, 25, 35, 49, 9, 23, 12, 18, 45, 27, 44]             
312
Company ID 38 will distribute shares to [28, 37, 47, 10, 35, 32, 45, 39, 18, 12, 29, 4, 42, 2, 36, 44, 21, 19, 5]             
313
Company ID 39 will distribute shares to [32, 26, 6, 8, 20, 1, 12, 30, 0, 3, 23, 31, 44, 19, 18, 42, 46, 38, 40]             
314
Company ID 40 will distribute shares to [43, 15, 1, 24, 30, 48, 42, 17, 21, 49, 46, 9, 19, 31, 20, 8, 22, 35, 27]             
315
Company ID 41 will distribute shares to [15, 22, 46, 18, 38, 36, 47, 16, 32, 42, 34, 3, 17, 44, 14, 4, 11, 13, 40]             
316
Company ID 42 will distribute shares to [31, 3, 28, 48, 7, 13, 0, 22, 27, 46, 24, 38, 11, 30, 29, 16, 18, 49, 36]             
317
Company ID 43 will distribute shares to [9, 45, 18, 38, 8, 48, 39, 15, 42, 29, 0, 24, 35, 37, 17, 5, 22, 3, 41]             
318
Company ID 44 will distribute shares to [41, 4, 22, 39, 19, 29, 17, 8, 15, 47, 26, 0, 18, 3, 25, 35, 46, 12, 5]             
319
Company ID 45 will distribute shares to [26, 11, 28, 15, 29, 14, 43, 2, 6, 49, 34, 46, 48, 40, 24, 30, 8, 33, 5]             
320
Company ID 46 will distribute shares to [37, 33, 47, 16, 1, 32, 17, 22, 13, 3, 24, 34, 44, 48, 28, 31, 38, 23, 15]             
321
Company ID 47 will distribute shares to [46, 10, 5, 34, 8, 20, 45, 42, 11, 3, 24, 28, 4, 9, 13, 38, 49, 15, 32]             
322
Company ID 48 will distribute shares to [6, 24, 0, 45, 22, 43, 39, 4, 34, 5, 44, 33, 7, 28, 10, 31, 1, 12, 47]             
323
Company ID 49 will distribute shares to [37, 43, 8, 32, 28, 48, 16, 26, 38, 2, 39, 1, 29, 35, 22, 34, 42, 3, 36]             
324

325
Aggregating shares for each debtor
326

327
Aggregating shares for ID 0
328
Aggregating shares for ID 1
329
Aggregating shares for ID 2
330
Aggregating shares for ID 3
331
Aggregating shares for ID 4
332
Aggregating shares for ID 5
333
Aggregating shares for ID 6
334
Aggregating shares for ID 7
335
Aggregating shares for ID 8
336
Aggregating shares for ID 9
337
Aggregating shares for ID 10
338
Aggregating shares for ID 11
339
Aggregating shares for ID 12
340
Aggregating shares for ID 13
341
Aggregating shares for ID 14
342
Aggregating shares for ID 15
343
Aggregating shares for ID 16
344
Aggregating shares for ID 17
345
Aggregating shares for ID 18
346
Aggregating shares for ID 19
347
Aggregating shares for ID 20
348
Aggregating shares for ID 21
349
Aggregating shares for ID 22
350
Aggregating shares for ID 23
351
Aggregating shares for ID 24
352
Aggregating shares for ID 25
353
Aggregating shares for ID 26
354
Aggregating shares for ID 27
355
Aggregating shares for ID 28
356
Aggregating shares for ID 29
357
Aggregating shares for ID 30
358
Aggregating shares for ID 31
359
Aggregating shares for ID 32
360
Aggregating shares for ID 33
361
Aggregating shares for ID 34
362
Aggregating shares for ID 35
363
Aggregating shares for ID 36
364
Aggregating shares for ID 37
365
Aggregating shares for ID 38
366
Aggregating shares for ID 39
367
Aggregating shares for ID 40
368
Aggregating shares for ID 41
369
Aggregating shares for ID 42
370
Aggregating shares for ID 43
371
Aggregating shares for ID 44
372
Aggregating shares for ID 45
373
Aggregating shares for ID 46
374
Aggregating shares for ID 47
375
Aggregating shares for ID 48
376
Aggregating shares for ID 49
377

378
Uploading shares to the blockchain
379

380
Shares for ID 0 have been uploaded to the Blockchain
381
Shares for ID 1 have been uploaded to the Blockchain
382
Shares for ID 2 have been uploaded to the Blockchain
383
Shares for ID 3 have been uploaded to the Blockchain
384
Shares for ID 4 have been uploaded to the Blockchain
385
Shares for ID 5 have been uploaded to the Blockchain
386
Shares for ID 6 have been uploaded to the Blockchain
387
Shares for ID 7 have been uploaded to the Blockchain
388
Shares for ID 8 have been uploaded to the Blockchain
389
Shares for ID 9 have been uploaded to the Blockchain
390
Shares for ID 10 have been uploaded to the Blockchain
391
Shares for ID 11 have been uploaded to the Blockchain
392
Shares for ID 12 have been uploaded to the Blockchain
393
Shares for ID 13 have been uploaded to the Blockchain
394
Shares for ID 14 have been uploaded to the Blockchain
395
Shares for ID 15 have been uploaded to the Blockchain
396
Shares for ID 16 have been uploaded to the Blockchain
397
Shares for ID 17 have been uploaded to the Blockchain
398
Shares for ID 18 have been uploaded to the Blockchain
399
Shares for ID 19 have been uploaded to the Blockchain
400
Shares for ID 20 have been uploaded to the Blockchain
401
Shares for ID 21 have been uploaded to the Blockchain
402
Shares for ID 22 have been uploaded to the Blockchain
403
Shares for ID 23 have been uploaded to the Blockchain
404
Shares for ID 24 have been uploaded to the Blockchain
405
Shares for ID 25 have been uploaded to the Blockchain
406
Shares for ID 26 have been uploaded to the Blockchain
407
Shares for ID 27 have been uploaded to the Blockchain
408
Shares for ID 28 have been uploaded to the Blockchain
409
Shares for ID 29 have been uploaded to the Blockchain
410
Shares for ID 30 have been uploaded to the Blockchain
411
Shares for ID 31 have been uploaded to the Blockchain
412
Shares for ID 32 have been uploaded to the Blockchain
413
Shares for ID 33 have been uploaded to the Blockchain
414
Shares for ID 34 have been uploaded to the Blockchain
415
Shares for ID 35 have been uploaded to the Blockchain
416
Shares for ID 36 have been uploaded to the Blockchain
417
Shares for ID 37 have been uploaded to the Blockchain
418
Shares for ID 38 have been uploaded to the Blockchain
419
Shares for ID 39 have been uploaded to the Blockchain
420
Shares for ID 40 have been uploaded to the Blockchain
421
Shares for ID 41 have been uploaded to the Blockchain
422
Shares for ID 42 have been uploaded to the Blockchain
423
Shares for ID 43 have been uploaded to the Blockchain
424
Shares for ID 44 have been uploaded to the Blockchain
425
Shares for ID 45 have been uploaded to the Blockchain
426
Shares for ID 46 have been uploaded to the Blockchain
427
Shares for ID 47 have been uploaded to the Blockchain
428
Shares for ID 48 have been uploaded to the Blockchain
429
Shares for ID 49 have been uploaded to the Blockchain
430

431
Downloading shares from the blockchain
432

433
Shares downloaded [[1, 4083203708697199681964231501100549899951], [2, 4756736302252317133019594003541031803202], [3, 4226254756126859079671575987920354047135], [4, 4487677943370531302081253604574810853308], [5, 4657304609729875573838028332734622222871], [6, 4588975315314469358962348455071230702542], [7, 4220939548347290436228390669802381648709], [8, 4370041896354800407787917413584801118667], [9, 4593910403608521917556232643525057361319], [10, 4061841502342413081103342447646056410230], [11, 4340686451015009668443505495133308028329], [12, 4436384107485749535181251246228827048417], [13, 3724220268208714866142610189645200988175], [14, 4352386004244771662101648645770629992072], [15, 4644806492516991440861658768273679233786], [16, 4234894463558853522449828710186484179008], [17, 4682644643706808523057331108536232246953], [18, 4581591148754920078857883470362248005545], [19, 4266961282457784375997385990302933160521], [20, 4041921687625963196797723844267955331871]]
434

435
Secret recovered from shares downloaded is 20729562
436
Sume of receivabales = 20729562 is equal to  20729562
437
Test Suceeded
%
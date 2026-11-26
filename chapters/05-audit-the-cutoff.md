# Audit the cutoff, not just the totals

Suppose a controller receives a tidy statement package. The journal balances. The balance sheet balances. Direct and indirect operating cash agree. The displayed May profit is $285. All three checks really do pass, and the $285 is still wrong.

You will locate an error invisible to conservation checks, repair it without affecting the bank ledger, and design an independent test that would catch the same error next month.

## The flawed entry

The shop collected three $100 advances. Its batch posted this entry at May close:

```text
Debit   Customer advances   300
Credit  Service revenue     300
```

The batch keyed on payment records. The case rule keys on acceptance of completed work. In the [case slips](../data/may-close.json), job A was accepted May 25, job B May 29, and job C June 2. At May 31 only $200 should move out of advances. The ledger's $300 release is two valid postings plus one premature posting.

If the bad batch is already posted, debit service revenue and credit customer advances $100. If the batch has not been posted, approve only the $200 valid release. Do not do both. The correction does not touch cash, because the shop really did collect the advance in May.

## Why the three checks miss it

| Check | Premature recognition | Correct cutoff |
| --- | ---: | ---: |
| Adjusted trial balance, each side | 2,670 | 2,670 |
| Total assets | 2,185 | 2,185 |
| Total liabilities | 420 | 520 |
| Closing equity | 1,765 | 1,665 |
| Net income | 285 | 185 |
| Operating cash, direct and indirect | 230 | 230 |

Revenue and the advance liability both have credit balances; one is overstated by what the other is understated, so the trial-balance total is unchanged. The balance-sheet total also reconciles: $100 moved from a liability to earned equity. In indirect operating cash, the $100 extra profit is canceled by the $100 smaller increase in customer advances. Direct operating cash sees no change because neither posting changes cash.

This is an accounting version of testing your own answer with your own premise. A prettier report cannot supply evidence it never received.

## Design a check that can disagree

Take the May release list, not the May receipts list. For each advance released to revenue, find an independent record with the job ID, acceptance date and amount. Mark missing, duplicate or out-of-period evidence for review. Then go the other way: find valid May acceptances for previously recorded advances that were not released. The two directions catch different errors. Keep the original batch, the correction entry, and the evidence reference. A saved exception makes the decision inspectable; overwriting the record removes the trail.

No model can certify a fictional or unavailable record. If you use one for an optional critique, limit its input to the synthetic ledger, ask it to specify the evidence needed rather than invent evidence, and recompute the proposed correction yourself.

## Practice: a change that should affect June

Imagine job C was accepted June 2 exactly as stated and no refund occurred. In June the shop debits the advance liability and credits earned service revenue $100. It does not debit cash again. If evidence were missing instead of dated June 2, stop for review rather than treating missing information as a June acceptance. The decision concerns when the shop earned the amount, not whether the payment arrived.

Open the [unaided close brief](../practice/may-close.md) and rebuild the ledger from the source slips. Use the [answer key](../practice/may-close-key.md) only after recording your own proposed cutoff.

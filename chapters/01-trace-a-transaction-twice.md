# Trace a transaction twice

Suppose a repair shop buys $100 of replacement parts on account. The parts are on the shelf; no payment has left the bank. A bank-feed-only log misses the event. A spending log might describe the purchase as an expense. The ledger records a narrower pair of facts: the shop has more parts, and it owes the supplier.

By the end of this chapter, you can move from a source record to a balanced journal entry, post the entry to accounts, produce a trial balance, and say what balancing did not verify.

## Define a boundary before recording a number

An account collects changes to one kind of balance. Cash and inventory are assets: resources the business controls. A payable is a liability: an obligation of the business. Equity is the residual after subtracting liabilities from assets. Revenue and expenses change equity through the period's result. Borrowing also changes what the business owes. It does not, by itself, earn revenue.

The exercise uses a separate business ledger. A shop owner buying a personal lunch is not automatically a shop expense, even if the wrong card was used. Ask whose resource moved and why. The same discipline applies to time: the balance sheet reports the position at an instant; income describes activity over an interval.

## What the two sides are for

Debit and credit mean left and right. They do not mean bad and good or money in and money out. In these examples:

| Account kind | Increases with | Decreases with |
| --- | --- | --- |
| Assets and expenses | Debit | Credit |
| Liabilities, equity and revenue | Credit | Debit |

An entry can have several lines, but total debits must equal total credits. This is a conservation check on the recording rule. It is not a truth detector for the underlying document.

Work a small ledger before the month-long case. The shop opens with $400 contributed by its owner. It buys $100 of parts on credit, completes an inspection for $75 in cash, and pays $40 to the supplier. No parts were used in the inspection.

| Source event | Debit | Credit |
| --- | --- | --- |
| Owner contributes cash | Cash $400 | Owner capital $400 |
| Parts delivered on credit | Inventory $100 | Accounts payable $100 |
| Inspection completed and paid | Cash $75 | Service revenue $75 |
| Supplier payment | Accounts payable $40 | Cash $40 |

The payment settles part of a balance already recorded. Expensing it now would forget why the payable was created. The service receipt, by contrast, pays for work just completed.

## Post, then check

Start each account at zero. Post each line to its named account and net the two sides.

| Account | Debit balance | Credit balance |
| --- | ---: | ---: |
| Cash | 435 | |
| Inventory | 100 | |
| Accounts payable | | 60 |
| Owner capital | | 400 |
| Service revenue | | 75 |
| Total | 535 | 535 |

Read the table backward. Cash equals $400 + $75 − $40. The parts are still available; the $100 stays in inventory. The supplier is owed $60. At this point the abbreviated equation is $535 of assets = $60 of liabilities + $475 of equity, including the $75 earned in the period.

Now imagine the buyer never posts the parts invoice. Both sides of that entry disappear. The resulting $435 trial balance still balances, even though inventory and supplier obligations are wrong. Check the receiving slip and the supplier account. A second model repeating the same ledger arithmetic cannot recover the missing fact.

## Try it before looking

**Practice.** Keep the entry for the inspection and the entire $100 parts delivery, but suppose the supplier payment was $55. Write the changed journal entry and trial balance before reading the answer.

**Check.** Debit accounts payable and credit cash $55. Cash becomes $420 and accounts payable $45. Total debits and credits are each $520. Inventory, owner capital and earned revenue are unchanged. If your service revenue moves, you made a settlement act like a new trade.

**Transfer.** Suppose a loan supplies $200 to the account. Which account explains the deposit? What source record would distinguish it from a $200 service receipt? Put the answers on the page before opening [the timing chapter](02-recognize-the-event.md).

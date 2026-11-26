# Read the statements together

In the fictional shop's May accounts, profit is $185 and cash increases by $290. Neither number is the other's checksum. Profit includes work done but not fully paid. Cash includes a loan that has not earned anything. The useful question is where the difference came from.

You will build three views of the same ledger, demonstrate that the opening and closing balances agree with the flow statements, and explain the largest differences without a balancing plug.

## Start with three questions

1. **Income statement:** What did the shop earn and consume during May?
2. **Balance sheet:** What does it control and owe at May 31, and what is the residual?
3. **Cash-flow statement:** Where did cash actually come from, and where did it go?

Use the [case slips](../data/may-close.json), but try a cash schedule first: add only transactions that actually change the cash account. Opening cash is $1,000. May operating receipts are $180 from a completed repair paid immediately, $70 collected on the invoice for another completed repair, and $300 of customer advances. Operating cash paid is $120 for coverage, $120 for parts and $80 for wages. That leaves $230 of operating cash flow. The new equipment uses $240 of investing cash; borrowing brings in $300 of financing cash. The increase is $230 − $240 + $300 = $290.

The [IAS 7 overview](https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/) describes operating, investing and financing cash-flow categories and direct and indirect presentations. This simplified exercise has no tax, interest, or material noncash investing or financing event. A complete reporting framework or external filing involves requirements beyond this exercise.

## Revenue tells a different story

The shop earned $320 on the cash and billed repairs and $200 on two jobs initially paid in advance. The third advance remains unearned. Expense the $145 of issued parts, $60 of May coverage, $100 for May wages (including $20 unpaid), and $30 of equipment depreciation.

| Income statement, May | Amount |
| --- | ---: |
| Service revenue | 520 |
| Parts expense | (145) |
| Coverage expense | (60) |
| Wage expense | (100) |
| Depreciation expense | (30) |
| Net income | 185 |

Follow the leftovers. The shop ends May with $1,290 cash, $70 receivable, $75 inventory, and $60 prepaid coverage. It has $840 gross equipment and a $150 offset for accumulated depreciation, for $690 net equipment. Total assets: $2,185. It owes $100 for supplies, $100 of service to the remaining advance customer, $20 for wages and $300 on the loan. Liabilities: $520. Ending equity is opening equity of $1,480 plus $185 income, or $1,665. There are no owner contributions or draws during May. $520 + $1,665 reconciles to $2,185.

## Reconcile operating cash another way

Start with $185 net income. Add back $30 depreciation, which reduced income without a May cash payment. Subtract $70 more receivables, $75 more inventory and $60 more prepaid coverage. Add $100 more accounts payable, $100 more customer advances and $20 more wages payable. These are operating changes relative to opening zero balances for those accounts:

```text
185 + 30 − 70 − 75 − 60 + 100 + 100 + 20 = 230
```

The bridge reaches the same operating cash as the bank-derived schedule. It does not include the loan proceeds or equipment purchase. Those appear elsewhere in the cash-flow statement. This is why treating all liabilities and assets as one working-capital adjustment would be wrong: the changes have different sources and classifications.

## Close the temporary balances

Revenue and expense are period counters. Following May reporting, close the $520 revenue and $335 expenses to equity, by way of a closing account if your ledger uses one. May income adds $185 to equity. Cash, receivables, inventory, prepayments, equipment, accumulated depreciation and liabilities carry forward. June starts its own revenue and expense counters at zero. Closing entries are not additional cash flows or expenses.

## Try it

If the $70 collection arrives June 1 instead, trace the May effects. Net income remains $185. May cash falls to $1,220 and receivables rise to $140; total assets do not change. Operating cash falls to $160 in both presentations. That is evidence you moved the collection, not the earned work.

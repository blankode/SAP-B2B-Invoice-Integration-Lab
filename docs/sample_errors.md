# Sample Error Scenarios

## Missing amount

Input:

```text
input/invoice_ubl_invalid_missing_amount.xml
```

Expected result:

```text
Status: FAILED
Error: Missing mandatory field: total_amount
```

## Unknown document type

Create a random `.txt` file and run:

```bash
python main.py input/random.txt
```

Expected result:

```text
Status: FAILED
Error: Unknown or unsupported document type
```

## Bad date

Change `IssueDate` to:

```xml
<IssueDate>20-06-2026</IssueDate>
```

Expected result:

```text
Issue date must use YYYY-MM-DD format
```

# How to run the main?

To call the main method in the terminal, run the command below from the project root:

    python -m src.main.main

Then, paste the JSON lists (one per line) and press Ctrl+D (Linux/Mac) or Ctrl+Z followed by Enter (Windows) to finish the input.

Example:

[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
[{"operation":"buy", "unit-cost":20.00, "quantity": 10000},{"operation":"sell", "unit-cost":10.00, "quantity": 5000}]

# How to run unit tests?

Run from the project root:

To run all tests:

    python -m unittest discover -s src/test -p "*.py"

To run a specific test:

    python -m src.test.service.test_operation_service

# Architecture Overview

mermaid
flowchart TD
    subgraph CLI/API
        A[main.py]
    end
    subgraph Domain
        B[OperationService]
        C[TaxService]
        D[OperationDto / OperationTaxDto]
        E[OperationUtil]
    end
    subgraph Infra
        F[config/TaxConfig.py]
        G[enum/OperationTypeEnum.py]
    end
    A -->|stdin JSON| E
    E -->|list of DTOs| B
    B --> C
    C --> D
    B --> D
    F -.-> C
    G -.-> D

**Summary:**  
- `main.py` receives operations via stdin, and uses `OperationUtil` to format the data.
- `OperationService` processes the operations, delegating tax calculation to `TaxService`.
- DTOs (`OperationDto`, `OperationTaxDto`) standardize the data.
- Configurations and enums centralize rules and types.

# Business Rules and Input/Output Examples

## Business Rules

- **Operation Types:** Only "buy" and "sell" operations are supported.
- **Weighted Average Price:**  
  - When buying, recalculate the weighted average price:  
    ```
    new_avg = ((current_qty * current_avg) + (buy_qty * buy_price)) / (current_qty + buy_qty)
    ```
- **Tax Calculation:**  
  - Tax is 20% (`TAX_PERCENTAGE`) over the profit of a sell operation, if the sell price > weighted average buy price.
  - No tax is paid if the total value of the sell operation (`unit_cost * quantity`) is less than or equal to 20,000.00.
  - Losses (when selling below average) are accumulated and used to offset future profits.
  - Losses are only deducted from profits if the sell operation value is above 20,000.00.
  - No tax is paid on buy operations.
  - If there is accumulated loss, it is deducted from the next profit(s) until exhausted.

## Input Example

Each line is a JSON array of operations:

[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}] 
[{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]

## Output Example

The output is a list of lists, each containing tax results for the corresponding input line:

[[{"tax": 0.0}, {"tax": 10000.0}], [{"tax": 0.0}, {"tax": 0.0}]]

## Example Scenario

Given the following operations:

[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}] [{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]

- The first "buy" sets the average price to 10.00.
- The first "sell" is at 20.00, profit per share is 10.00, total profit is 50,000.00. Tax is 20% of 50,000.00 = 10,000.00.
- The second "buy" updates the average price.
- The second "sell" is at 10.00, which may result in no tax if there is no profit.

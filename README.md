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

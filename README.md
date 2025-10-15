# Fence Test

## Technical Exercise Instructions
### Objective
This exercise is designed to serve as the basis for a technical discussion in the next interview step. It is not intended to take more than 2–4 hours. Please prioritize clarity of thought and decision-making over completeness or perfection.

Feel free to use any AI.

### Deliverables
- A Smart Contract with functions to update and read the interest rate
- A FastAPI application exposing 2 endpoints
  - POST /asset
    - Receive a list of assets and updates the average interest rate in the Smart Contract
    - Example payload
```
[
	{"id": "id-1", "interest_rate": 100},
	{"id": "id-2", "interest_rate": 10}
]
```
  - GET /interest_rate
    - Returns the interest rate value currently stored in the Smart Contract
- A README describing
  - Your reasoning and assumptions.
  - Trade-offs you considered.
  - How you would productionize your solution.
  - Any relevant setup or usage instructions.

> **Note:** If implementing the Smart Contract part becomes too time-consuming or complex, it’s perfectly fine to store and manage the data in a database instead. What matters most is the structure and reasoning behind your solution.


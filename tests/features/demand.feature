Feature: Demand is met at the least discounted cost
  OSeMOSYS meets the specified annual demand for each fuel in every time slice
  (EQ_SpecifiedDemand, EBa9, EBa11), and the accumulated annual demand over the
  year (EBb4), from whichever technologies produce the fuel most cheaply.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020, 2021, 2022
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds GAS, COAL
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | *          | ELC  | 1                 | *    | 1     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | 1                 | *    | 2     |
      | R1     | COAL       | 1                 | *    | 1     |

  Scenario: The cheaper technology meets the whole demand, shaped by its profile
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | DAY       | *    | 0.6   |
      | R1     | ELC  | NIGHT     | *    | 0.4   |
    When the model is solved
    Then RateOfDemand is
      | REGION | TIMESLICE | FUEL | YEAR | VALUE |
      | R1     | DAY       | ELC  | *    | 120   |
      | R1     | NIGHT     | ELC  | *    | 80    |
    And ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | DAY       | COAL       | ELC  | *    | 60    |
      | R1     | NIGHT     | COAL       | ELC  | *    | 40    |
      | R1     | *         | GAS        | ELC  | *    | 0     |
    And the objective is 279.0498848

  Scenario: A technology that does not run at night cannot meet a demand at night
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | *         | *    | 0.5   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | *          | NIGHT     | *    | 0     |
    When the model is solved
    Then the model is infeasible

  Scenario: An accumulated annual demand may be met in any time slice
    Given AccumulatedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | *          | NIGHT     | *    | 0     |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | DAY       | COAL       | ELC  | *    | 100   |
      | R1     | NIGHT     | COAL       | ELC  | *    | 0     |
    And the objective is 279.0498848

  Scenario: A technology's input is produced upstream in proportion to its activity
    Given the set FUEL holds ELC, NGAS
    And the set TECHNOLOGY holds GAS, WELL
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | ELC  | 1                 | *    | 1     |
      | R1     | WELL       | NGAS | 1                 | *    | 1     |
    And InputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | NGAS | 1                 | *    | 2     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | 1                 | *    | 2     |
    When the model is solved
    Then ProductionAnnual is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
      | R1     | NGAS | *    | 200   |
    And UseAnnual is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | NGAS | *    | 200   |
    And the objective is 558.0997696

Feature: Regions trade fuel along their trade routes
  OSeMOSYS lets a region send a fuel to another region where a trade route
  joins them. What one region sends the other receives (EBa10), and the trade
  enters the balance of each time slice (EBa11) and, summed over the year
  (EBb3), the annual balance (EBb4).

  Background:
    Given the set REGION holds R1, R2
    And the set YEAR holds 2020
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds COAL, GAS
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | COAL       | ELC  | 1                 | *    | 1     |
      | R2     | GAS        | ELC  | 1                 | *    | 1     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | COAL       | 1                 | *    | 1     |
      | R2     | GAS        | 1                 | *    | 2     |

  Scenario: A region meets its demand with fuel from a cheaper region along a trade route
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R2     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R2     | ELC  | *         | *    | 0.5   |
    And TradeRoute is
      | REGION | _REGION | FUEL | YEAR | VALUE |
      | R1     | R2      | ELC  | *    | 1     |
      | R2     | R1      | ELC  | *    | 1     |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | *    | 50    |
      | R2     | *         | GAS        | ELC  | *    | 0     |
    And the objective is 97.5900073

  Scenario: Without a trade route a region cannot import fuel
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R2     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R2     | ELC  | *         | *    | 0.5   |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | *    | 0     |
      | R2     | *         | GAS        | ELC  | *    | 50    |
    And the objective is 195.1800146

  Scenario: What a region sends along a trade route its partner receives in the same time slice
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | *      | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | *      | ELC  | *         | *    | 0.5   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | COAL       | NIGHT     | *    | 0     |
      | R2     | GAS        | DAY       | *    | 0     |
    And TradeRoute is
      | REGION | _REGION | FUEL | YEAR | VALUE |
      | R1     | R2      | ELC  | *    | 1     |
      | R2     | R1      | ELC  | *    | 1     |
    When the model is solved
    Then Trade is
      | REGION | _REGION | TIMESLICE | FUEL | YEAR | VALUE |
      | R1     | R2      | DAY       | ELC  | *    | 50    |
      | R1     | R2      | NIGHT     | ELC  | *    | -50   |
      | R2     | R1      | DAY       | ELC  | *    | -50   |
      | R2     | R1      | NIGHT     | ELC  | *    | 50    |
    And TradeAnnual is
      | REGION | _REGION | FUEL | YEAR | VALUE |
      | R1     | R2      | ELC  | *    | 0     |
      | R2     | R1      | ELC  | *    | 0     |
    And the objective is 292.7700219

  Scenario: An accumulated annual demand may be met with fuel imported in any time slice
    Given AccumulatedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R2     | ELC  | *    | 100   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | COAL       | NIGHT     | *    | 0     |
    And TradeRoute is
      | REGION | _REGION | FUEL | YEAR | VALUE |
      | R1     | R2      | ELC  | *    | 1     |
      | R2     | R1      | ELC  | *    | 1     |
    When the model is solved
    Then Trade is
      | REGION | _REGION | TIMESLICE | FUEL | YEAR | VALUE |
      | R1     | R2      | DAY       | ELC  | *    | 100   |
      | R1     | R2      | NIGHT     | ELC  | *    | 0     |
    And TradeAnnual is
      | REGION | _REGION | FUEL | YEAR | VALUE |
      | R1     | R2      | ELC  | *    | 100   |
      | R2     | R1      | ELC  | *    | -100  |
    And ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R2     | *         | GAS        | ELC  | *    | 0     |
    And the objective is 97.5900073

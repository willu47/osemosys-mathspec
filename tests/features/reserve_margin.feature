Feature: Tagged capacity stands behind peak production by the reserve margin
  OSeMOSYS sums the capacity of the technologies ReserveMarginTagTechnology tags, each in
  proportion to its tag (RM1), and the production rate of the fuels ReserveMarginTagFuel tags
  in each time slice (RM2). In every time slice that capacity is at least the production rate
  times the ReserveMargin (RM3), so it stands behind the peak production rate.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds GAS, SOLAR
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | *          | ELC  | 1                 | *    | 1     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | DAY       | *    | 0.6   |
      | R1     | ELC  | NIGHT     | *    | 0.4   |
    And CapitalCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 10    |
      | R1     | SOLAR      | *    | 20    |
    And ReserveMargin is
      | REGION | YEAR | VALUE |
      | R1     | *    | 1.2   |
    And ReserveMarginTagFuel is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 1     |

  Scenario: Tagged capacity is the peak production rate times the reserve margin
    Given ReserveMarginTagTechnology is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 1     |
    When the model is solved
    Then TotalCapacityAnnual is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 144   |
      | R1     | SOLAR      | *    | 0     |
    And the objective is 1440

  Scenario: Capacity of an untagged technology does not count towards the reserve margin
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | SOLAR      | *    | 200   |
    And ReserveMarginTagTechnology is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 1     |
      | R1     | SOLAR      | *    | 0     |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 144   |
      | R1     | SOLAR      | *    | 0     |
    And the objective is 1440

  Scenario: A technology tagged in part counts that share of its capacity towards the reserve margin
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | SOLAR      | *    | 200   |
    And ReserveMarginTagTechnology is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 1     |
      | R1     | SOLAR      | *    | 0.5   |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 44    |
      | R1     | SOLAR      | *    | 0     |
    And the objective is 440

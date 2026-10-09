Feature: A technology's capacity and activity stay within their limits
  OSeMOSYS bounds each technology's total capacity in a year (TCC1, TCC2), its
  new capacity in a year (NCC1, NCC2), its activity in a year (AAC1 to AAC3) and
  its activity over the model period (TAC1 to TAC3). A limit of -1 sets no limit.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020, 2021
    And the set TIMESLICE holds ALLYEAR
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds GAS, COAL
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | ALLYEAR   | *    | 1     |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | *          | ELC  | 1                 | *    | 1     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | 1                 | *    | 2     |
      | R1     | COAL       | 1                 | *    | 1     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | ALLYEAR   | *    | 1     |

  Scenario Outline: An upper limit on capacity or activity caps the cheaper technology and the dearer one meets the rest
    Given <limit> is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 60    |
    When the model is solved
    Then TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 60    |
      | R1     | GAS        | *    | 40    |
    And the objective is 266.7460199

    Examples:
      | limit                                   |
      | TotalAnnualMaxCapacity                  |
      | TotalTechnologyAnnualActivityUpperLimit |

  Scenario Outline: A minimum total or new capacity is built and paid for even where it never runs
    Given <limit> is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | 2020 | 30    |
    And CapitalCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 10    |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | 2020 | 30    |
      | R1     | GAS        | 2021 | 0     |
    And TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 100   |
      | R1     | GAS        | *    | 0     |
    And the objective is 490.5328714

    Examples:
      | limit                            |
      | TotalAnnualMinCapacity           |
      | TotalAnnualMinCapacityInvestment |

  Scenario: A cap on new capacity leaves the residual capacity free to run
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 50    |
    And TotalAnnualMaxCapacityInvestment is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 20    |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 20    |
    And TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 70    |
      | R1     | GAS        | *    | 30    |
    And the objective is 247.6927328

  Scenario: An annual activity lower limit makes the dearer technology run in that year
    Given TotalTechnologyAnnualActivityLowerLimit is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | 2021 | 30    |
    When the model is solved
    Then TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | 2020 | 100   |
      | R1     | COAL       | 2021 | 70    |
      | R1     | GAS        | 2020 | 0     |
      | R1     | GAS        | 2021 | 30    |
    And the objective is 218.4157306

  Scenario: A model-period activity upper limit is spent in the earliest year, where it saves the most
    Given TotalTechnologyModelPeriodActivityUpperLimit is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | COAL       | 150   |
    When the model is solved
    Then TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | 2020 | 100   |
      | R1     | COAL       | 2021 | 50    |
      | R1     | GAS        | 2020 | 0     |
      | R1     | GAS        | 2021 | 50    |
    And TotalTechnologyModelPeriodActivity is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | COAL       | 150   |
      | R1     | GAS        | 50    |
    And the objective is 237.0043034

  Scenario: A model-period activity lower limit is met in the latest year, where it costs the least
    Given TotalTechnologyModelPeriodActivityLowerLimit is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | GAS        | 30    |
    When the model is solved
    Then TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | 2020 | 100   |
      | R1     | COAL       | 2021 | 70    |
      | R1     | GAS        | 2020 | 0     |
      | R1     | GAS        | 2021 | 30    |
    And TotalTechnologyModelPeriodActivity is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | GAS        | 30    |
    And the objective is 218.4157306

  Scenario: A maximum capacity of zero rules a technology out, and one of -1 sets no limit
    Given TotalAnnualMaxCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | 2020 | 0     |
      | R1     | COAL       | 2021 | -1    |
    When the model is solved
    Then TotalTechnologyAnnualActivity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | 2020 | 0     |
      | R1     | COAL       | 2021 | 100   |
      | R1     | GAS        | 2020 | 100   |
      | R1     | GAS        | 2021 | 0     |
    And the objective is 288.1228787

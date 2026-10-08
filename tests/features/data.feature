Feature: The data is checked and completed before the model is built
  Before it solves, OSeMOSYS checks that the year split sums to one in each year ('Time Slice'
  check) and that a technology's limits do not contradict each other ('Capacity investment',
  'Annual Activity' and 'Minimum Annual activity' checks). No check compares a maximum capacity
  with a minimum capacity. The declarations of RETagTechnology (binary) and
  ReserveMarginTagTechnology (between 0 and 1) refuse a tag outside that domain. A row the data
  leaves out takes the parameter's default. A block the data does not use can be left out of the
  model, and the model then solves at the same cost.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds GAS
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | ELC  | 1                 | *    | 1     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | *         | *    | 0.5   |
    And CapitalCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 1     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | 1                 | *    | 1     |

  Scenario: A year split that does not sum to one is refused
    Given YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | DAY       | *    | 0.5   |
      | NIGHT     | *    | 0.4   |
    When the model is solved
    Then the data is refused for "year_split_sums_to_one"

  Scenario Outline: Limits on a technology that cannot both hold are refused
    Given <upper> is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 10    |
    And <lower> is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 20    |
    When the model is solved
    Then the data is refused for "<check>"

    Examples:
      | upper                                   | lower                                   | check                                   |
      | TotalAnnualMaxCapacityInvestment        | TotalAnnualMinCapacityInvestment        | capacity_investment_bounds_do_not_cross |
      | TotalTechnologyAnnualActivityUpperLimit | TotalTechnologyAnnualActivityLowerLimit | annual_activity_limits_do_not_cross     |
      | TotalAnnualMaxCapacity                  | TotalTechnologyAnnualActivityLowerLimit | max_capacity_can_meet_min_activity      |

  Scenario: A maximum capacity below the minimum capacity is not checked, so the model is infeasible
    Given TotalAnnualMaxCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 150   |
    And TotalAnnualMinCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 160   |
    When the model is solved
    Then the model is infeasible

  Scenario Outline: A tag outside its MathProg domain is refused
    Given <tag> is
      | REGION | TECHNOLOGY | YEAR | VALUE   |
      | R1     | GAS        | *    | <value> |
    When the model is solved
    Then the data is refused for "<check>"

    Examples:
      | tag                        | value | check                                    |
      | RETagTechnology            | 0.5   | re_tag_technology_is_binary              |
      | ReserveMarginTagTechnology | 1.5   | reserve_margin_tag_technology_is_a_share |

  Scenario: A row the data leaves out takes the parameter's default, not zero
    Given SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | DAY       | *    | 0.2   |
      | R1     | ELC  | NIGHT     | *    | 0.8   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | GAS        | DAY       | *    | 0.5   |
    When the model is solved
    Then TotalCapacityAnnual is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 160   |
    And the objective is 257.5900073

  Scenario: The whole model meets the demand at its capital cost plus its discounted variable cost
    When the model is solved
    Then TotalCapacityAnnual is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | GAS        | *    | 100   |
    And the objective is 197.5900073

  Scenario Outline: The model solves at the same cost without a block the data does not use
    Given the model leaves out the <block> block
    When the model is solved
    Then the objective is 197.5900073

    Examples:
      | block          |
      | trade          |
      | storage        |
      | limits         |
      | reserve margin |
      | re target      |
      | emissions      |

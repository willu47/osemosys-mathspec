Feature: Capacity covers the activity in every time slice
  OSeMOSYS keeps a technology's rate of activity, summed over its modes (CAa3), within
  its capacity times its capacity factor and CapacityToActivityUnit in each time slice
  (CAa4), and within its availability over the year (CAb1). Its capacity is the residual
  capacity plus what it built within its operational life (CAa1, CAa2), in whole units (CAa5).

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds PLANT
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | PLANT      | ELC  | 1                 | *    | 1     |
    And CapitalCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 1     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | DAY       | *    | 0.8   |
      | R1     | ELC  | NIGHT     | *    | 0.2   |

  Scenario: Capacity covers the peak rate of activity, not the average
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 160   |
    And the objective is 160

  Scenario: Capacity allows its capacity factor times CapacityToActivityUnit of activity in each time slice
    Given CapacityToActivityUnit is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 10    |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | PLANT      | DAY       | *    | 1     |
      | R1     | PLANT      | NIGHT     | *    | 0.1   |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 40    |
    And the objective is 40

  Scenario: Planned maintenance limits the activity over the year, not in each time slice
    Given AvailabilityFactor is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 0.5   |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 200   |
    And the objective is 200

  Scenario: Residual capacity is used before new capacity is built
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 60    |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 100   |
    And TotalCapacityAnnual is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 160   |
    And the objective is 100

  Scenario: New capacity retires at the end of its operational life
    Given the set YEAR holds 2020, 2021, 2022, 2023
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | *         | *    | 0.5   |
    And OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 2     |
    When the model is solved
    Then NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 100   |
      | R1     | PLANT      | 2021 | 0     |
      | R1     | PLANT      | 2022 | 100   |
      | R1     | PLANT      | 2023 | 0     |
    And TotalCapacityAnnual is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 100   |
    And the objective is 190.7029478

  Scenario: Capacity comes in whole units where a unit size is given
    Given CapacityOfOneTechnologyUnit is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 30    |
    When the model is solved
    Then NumberOfNewTechnologyUnits is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 6     |
    And NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 180   |
    And the objective is 180

  Scenario: A technology's modes of operation share its capacity
    Given the set MODE_OF_OPERATION holds 1, 2
    And the set FUEL holds ELC, HEAT
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | PLANT      | ELC  | 1                 | *    | 1     |
      | R1     | PLANT      | HEAT | 2                 | *    | 1     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | *    | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | DAY       | *    | 0.8   |
      | R1     | ELC  | NIGHT     | *    | 0.2   |
      | R1     | HEAT | DAY       | *    | 0.2   |
      | R1     | HEAT | NIGHT     | *    | 0.8   |
    When the model is solved
    Then RateOfActivity is
      | REGION | TIMESLICE | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | DAY       | PLANT      | 1                 | 2020 | 160   |
      | R1     | DAY       | PLANT      | 2                 | 2020 | 40    |
      | R1     | NIGHT     | PLANT      | 1                 | 2020 | 40    |
      | R1     | NIGHT     | PLANT      | 2                 | 2020 | 160   |
    And NewCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 200   |
    And the objective is 200

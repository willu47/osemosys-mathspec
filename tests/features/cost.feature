Feature: Costs are discounted to the first year, less the salvage value
  OSeMOSYS pays a technology's capital cost in the year it is built, as an annuity over its
  operational life at the technology's own discount rate, discounted back to the year of build
  at the region's rate (CC1), and then from the start of that year to the first year (CC2). It
  pays the operating costs each year, discounted from the middle of the year (OC1 to OC4).
  Capacity that outlives the model period is credited its salvage value, discounted from the
  end of the period (SV1 to SV4).

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020, 2021, 2022
    And the set TIMESLICE holds ALLYEAR
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds PLANT
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | ALLYEAR   | *    | 1     |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | PLANT      | ELC  | 1                 | *    | 1     |
    And CapitalCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 100   |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 10    |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | ALLYEAR   | *    | 1     |

  Scenario: Capital cost is paid in full in the year of build, discounted from the start of that year
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | 2021 | 10    |
      | R1     | ELC  | 2022 | 10    |
    And OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 2     |
    When the model is solved
    Then CapitalInvestment is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 0     |
      | R1     | PLANT      | 2021 | 1000  |
      | R1     | PLANT      | 2022 | 0     |
    And DiscountedCapitalInvestment is
      | REGION | TECHNOLOGY | YEAR | VALUE       |
      | R1     | PLANT      | 2021 | 952.3809524 |
    And the objective is 952.3809524

  Scenario: Fixed cost is paid each year on all capacity in service, used or not
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 20    |
    And FixedCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 3     |
    When the model is solved
    Then AnnualFixedOperatingCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 60    |
    And the objective is 167.4299309

  Scenario: Operating cost is discounted to the first year from the middle of each year
    Given ResidualCapacity is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 10    |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | PLANT      | 1                 | *    | 1     |
    When the model is solved
    Then OperatingCost is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | *    | 10    |
    And DiscountedOperatingCost is
      | REGION | TECHNOLOGY | YEAR | VALUE       |
      | R1     | PLANT      | 2020 | 9.759000729 |
      | R1     | PLANT      | 2021 | 9.294286409 |
      | R1     | PLANT      | 2022 | 8.851701342 |
    And the objective is 27.90498848

  Scenario: Capacity that outlives the model period is credited its sinking-fund salvage value
    Given OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 4     |
    When the model is solved
    Then SalvageValue is
      | REGION | TECHNOLOGY | YEAR | VALUE       |
      | R1     | PLANT      | 2020 | 268.5826977 |
    And DiscountedSalvageValue is
      | REGION | TECHNOLOGY | YEAR | VALUE       |
      | R1     | PLANT      | 2020 | 232.0118326 |
    And the objective is 767.9881674

  Scenario: Straight-line depreciation credits the share of the life left after the model period
    Given DepreciationMethod is
      | REGION | VALUE |
      | R1     | 2     |
    And OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 4     |
    When the model is solved
    Then SalvageValue is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 250   |
    And the objective is 784.0406004

  Scenario: Capacity whose life ends within the model period has no salvage value
    Given OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 3     |
    When the model is solved
    Then SalvageValue is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | PLANT      | 2020 | 0     |
    And the objective is 1000

  Scenario: A technology's own discount rate above the region's raises its capital investment
    Given SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | 2020 | 10    |
    And OperationalLife is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 2     |
    And DiscountRateIdv is
      | REGION | TECHNOLOGY | VALUE |
      | R1     | PLANT      | 0.1   |
    When the model is solved
    Then CapitalInvestment is
      | REGION | TECHNOLOGY | YEAR | VALUE       |
      | R1     | PLANT      | 2020 | 1022.675737 |
    And the objective is 1022.675737

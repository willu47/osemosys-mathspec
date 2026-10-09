Feature: Storage moves energy between time slices
  OSeMOSYS lets a technology charge a storage in one mode and discharge it in another
  (S1, S2). The net charge sets the storage level at each chronological
  boundary (S3 to S15), which stays between the minimum charge and the capacity
  (SC1 to SC4, SI1, SI2). Charge and discharge rates stay within their limits
  (SC5, SC6), and new storage capacity costs a discounted investment (SI4 to SI10).
  Each of the two daily time brackets lasts half a day: its DaySplit of 0.00137 is
  12 h of the 8760 h in a year.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020, 2021
    And the set TIMESLICE holds DAY, NIGHT
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds SOLAR, GAS, BATTERY
    And the set MODE_OF_OPERATION holds 1, 2
    And the set DAILYTIMEBRACKET holds 1, 2
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | *         | *    | 0.5   |
    And Conversionls is
      | TIMESLICE | SEASON | VALUE |
      | *         | 1      | 1     |
    And Conversionld is
      | TIMESLICE | DAYTYPE | VALUE |
      | *         | 1       | 1     |
    And Conversionlh is
      | TIMESLICE | DAILYTIMEBRACKET | VALUE |
      | DAY       | 1                | 1     |
      | NIGHT     | 2                | 1     |
    And DaySplit is
      | DAILYTIMEBRACKET | YEAR | VALUE   |
      | *                | *    | 0.00137 |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | *         | *    | 0.5   |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | SOLAR      | ELC  | 1                 | *    | 1     |
      | R1     | GAS        | ELC  | 1                 | *    | 1     |
      | R1     | BATTERY    | ELC  | 2                 | *    | 1     |
    And InputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | BATTERY    | ELC  | 1                 | *    | 1     |
    And TechnologyToStorage is
      | REGION | TECHNOLOGY | STORAGE | MODE_OF_OPERATION | VALUE |
      | R1     | BATTERY    | DAM     | 1                 | 1     |
    And TechnologyFromStorage is
      | REGION | TECHNOLOGY | STORAGE | MODE_OF_OPERATION | VALUE |
      | R1     | BATTERY    | DAM     | 2                 | 1     |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | SOLAR      | 1                 | *    | 1     |
      | R1     | GAS        | 1                 | *    | 3     |
      | R1     | BATTERY    | 2                 | *    | 0.5   |
    And CapacityFactor is
      | REGION | TECHNOLOGY | TIMESLICE | YEAR | VALUE |
      | R1     | SOLAR      | NIGHT     | *    | 0     |
    And StorageMaxChargeRate is
      | REGION | STORAGE | VALUE |
      | R1     | DAM     | 1000  |
    And StorageMaxDischargeRate is
      | REGION | STORAGE | VALUE |
      | R1     | DAM     | 1000  |

  Scenario: Storage carries cheap daytime energy into the night
    When the model is solved
    Then RateOfStorageCharge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE |
      | R1     | DAM     | *      | *       | 1                | *    | 100   |
      | R1     | DAM     | *      | *       | 2                | *    | 0     |
    And RateOfStorageDischarge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE |
      | R1     | DAM     | *      | *       | 1                | *    | 0     |
      | R1     | DAM     | *      | *       | 2                | *    | 100   |
    And ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | DAY       | SOLAR      | ELC  | *    | 100   |
      | R1     | *         | GAS        | ELC  | *    | 0     |
    And the objective is 238.1660892

  Scenario: The storage spends StorageLevelStart in the first year before it charges
    Given StorageLevelStart is
      | REGION | STORAGE | VALUE |
      | R1     | DAM     | 50    |
    When the model is solved
    Then StorageLevelYearStart is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | 2020 | 50    |
      | R1     | DAM     | 2021 | 0     |
    And RateOfStorageCharge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE |
      | R1     | DAM     | *      | *       | 1                | 2020 | 0     |
      | R1     | DAM     | *      | *       | 1                | 2021 | 100   |
    And the objective is 189.3710856

  Scenario Outline: The storage moves no more than its maximum charge or discharge rate allows
    Given <rate limit> is
      | REGION | STORAGE | VALUE  |
      | R1     | DAM     | <rate> |
    When the model is solved
    Then RateOfStorageCharge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE  |
      | R1     | DAM     | *      | *       | 1                | *    | <rate> |
    And RateOfStorageDischarge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE  |
      | R1     | DAM     | *      | *       | 2                | *    | <rate> |
    And ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE          |
      | R1     | NIGHT     | GAS        | ELC  | *    | <gas at night> |
    And the objective is <objective>

    Examples:
      | rate limit              | rate | gas at night | objective   |
      | StorageMaxChargeRate    | 40   | 30           | 323.9058814 |
      | StorageMaxDischargeRate | 60   | 20           | 295.3259506 |

  Scenario: The storage level never falls below its minimum charge
    Given StorageLevelStart is
      | REGION | STORAGE | VALUE |
      | R1     | DAM     | 550   |
    And ResidualStorageCapacity is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 1000  |
    And MinStorageCharge is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 0.5   |
    When the model is solved
    Then StorageLevelYearFinish is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 500   |
    And RateOfStorageDischarge is
      | REGION | STORAGE | SEASON | DAYTYPE | DAILYTIMEBRACKET | YEAR | VALUE |
      | R1     | DAM     | *      | *       | 1                | *    | 0     |
      | R1     | DAM     | *      | *       | 2                | *    | 100   |
    And the objective is 189.3710856

  Scenario: New storage capacity costs its capital cost discounted from the start of the year it is built
    Given ResidualStorageCapacity is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 0     |
    And OperationalLifeStorage is
      | REGION | STORAGE | VALUE |
      | R1     | DAM     | 1     |
    And CapitalCostStorage is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 100   |
    When the model is solved
    Then NewStorageCapacity is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | *    | 0.137 |
    And DiscountedCapitalInvestmentStorage is
      | REGION | STORAGE | YEAR | VALUE |
      | R1     | DAM     | 2020 | 13.7  |
      | R1     | DAM     | 2021 | 13.047619 |
    And the objective is 264.9137083

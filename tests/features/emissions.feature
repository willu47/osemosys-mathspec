Feature: Emissions follow activity, stay within their limits and are penalised
  OSeMOSYS counts each technology's emission as its activity times its emission
  activity ratio (E1, E2, E6, E7), caps the emission of each year and of the model
  period, exogenous emission included (E8, E9), and adds the emissions penalty,
  discounted from the middle of the year, to the technology's cost (E3 to E5, TDC1).

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
    And EmissionActivityRatio is
      | REGION | TECHNOLOGY | EMISSION | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | GAS        | CO2      | 1                 | *    | 1     |
      | R1     | COAL       | CO2      | 1                 | *    | 2     |
    And SpecifiedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And SpecifiedDemandProfile is
      | REGION | FUEL | TIMESLICE | YEAR | VALUE |
      | R1     | ELC  | ALLYEAR   | *    | 1     |

  Scenario: A technology emits its activity times its emission activity ratio
    When the model is solved
    Then AnnualTechnologyEmission is
      | REGION | TECHNOLOGY | EMISSION | YEAR | VALUE |
      | R1     | COAL       | CO2      | *    | 200   |
      | R1     | GAS        | CO2      | *    | 0     |
    And AnnualEmissions is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | *    | 200   |
    And ModelPeriodEmissions is
      | REGION | EMISSION | VALUE |
      | R1     | CO2      | 400   |
    And the objective is 190.5328714

  Scenario: An annual emission limit makes the cleaner technology meet part of the demand
    Given AnnualEmissionLimit is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2021 | 150   |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | 2020 | 100   |
      | R1     | *         | COAL       | ELC  | 2021 | 50    |
      | R1     | *         | GAS        | ELC  | 2020 | 0     |
      | R1     | *         | GAS        | ELC  | 2021 | 50    |
    And AnnualEmissions is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2020 | 200   |
      | R1     | CO2      | 2021 | 150   |
    And the objective is 237.0043034

  Scenario: Annual exogenous emission uses up part of the annual emission limit
    Given AnnualEmissionLimit is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2021 | 150   |
    And AnnualExogenousEmission is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2021 | 30    |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | 2020 | 100   |
      | R1     | *         | COAL       | ELC  | 2021 | 20    |
      | R1     | *         | GAS        | ELC  | 2020 | 0     |
      | R1     | *         | GAS        | ELC  | 2021 | 80    |
    And AnnualEmissions is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2020 | 200   |
      | R1     | CO2      | 2021 | 120   |
    And the objective is 264.8871627

  Scenario: A model-period emission limit, less the exogenous emission, is spent in the earliest year
    Given ModelPeriodEmissionLimit is
      | REGION | EMISSION | VALUE |
      | R1     | CO2      | 300   |
    And ModelPeriodExogenousEmission is
      | REGION | EMISSION | VALUE |
      | R1     | CO2      | 50    |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | 2020 | 50    |
      | R1     | *         | COAL       | ELC  | 2021 | 0     |
      | R1     | *         | GAS        | ELC  | 2020 | 50    |
      | R1     | *         | GAS        | ELC  | 2021 | 100   |
    And ModelPeriodEmissions is
      | REGION | EMISSION | VALUE |
      | R1     | CO2      | 300   |
    And the objective is 332.2707391

  Scenario: The emissions penalty is discounted from the middle of the year and added to the cost
    Given EmissionsPenalty is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | *    | 0.5   |
    When the model is solved
    Then AnnualTechnologyEmissionsPenalty is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | COAL       | *    | 100   |
      | R1     | GAS        | *    | 0     |
    And DiscountedTechnologyEmissionsPenalty is
      | REGION | TECHNOLOGY | YEAR | VALUE      |
      | R1     | COAL       | 2020 | 97.5900073 |
      | R1     | COAL       | 2021 | 92.9428641 |
      | R1     | GAS        | *    | 0          |
    And the objective is 381.0657428

  Scenario: An emissions penalty high enough switches production to the cleaner technology
    Given EmissionsPenalty is
      | REGION | EMISSION | YEAR | VALUE |
      | R1     | CO2      | 2021 | 2     |
    When the model is solved
    Then ProductionByTechnology is
      | REGION | TIMESLICE | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | *         | COAL       | ELC  | 2020 | 100   |
      | R1     | *         | COAL       | ELC  | 2021 | 0     |
      | R1     | *         | GAS        | ELC  | 2020 | 0     |
      | R1     | *         | GAS        | ELC  | 2021 | 100   |
    And the objective is 469.3614637

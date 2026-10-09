Feature: Renewables make at least the target share of the tagged fuels' production
  OSeMOSYS adds up over the year what the technologies RETagTechnology tags produce (RE1, RE2)
  and the production of the fuels RETagFuel tags (RE3). The first is at least
  REMinProductionTarget times the second (RE4), so production without a tag does not count.

  Background:
    Given the set REGION holds R1
    And the set YEAR holds 2020
    And the set TIMESLICE holds ALLYEAR
    And the set FUEL holds ELC
    And the set TECHNOLOGY holds COAL, SOLAR
    And YearSplit is
      | TIMESLICE | YEAR | VALUE |
      | ALLYEAR   | *    | 1     |
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | *          | ELC  | 1                 | *    | 1     |
    And AccumulatedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | COAL       | 1                 | *    | 1     |
      | R1     | SOLAR      | 1                 | *    | 2     |
    And RETagFuel is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 1     |
    And REMinProductionTarget is
      | REGION | YEAR | VALUE |
      | R1     | *    | 0.4   |

  Scenario: Tagged renewables make the target share of the tagged fuel's production, and no more
    Given RETagTechnology is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | SOLAR      | *    | 1     |
    When the model is solved
    Then ProductionByTechnologyAnnual is
      | REGION | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | COAL       | ELC  | *    | 60    |
      | R1     | SOLAR      | ELC  | *    | 40    |
    And the objective is 136.6260102

  Scenario: Production of an untagged fuel does not raise the target
    Given the set FUEL holds ELC, HEAT
    And the set TECHNOLOGY holds COAL, SOLAR, BOILER
    And OutputActivityRatio is
      | REGION | TECHNOLOGY | FUEL | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | COAL       | ELC  | 1                 | *    | 1     |
      | R1     | SOLAR      | ELC  | 1                 | *    | 1     |
      | R1     | BOILER     | HEAT | 1                 | *    | 1     |
    And AccumulatedAnnualDemand is
      | REGION | FUEL | YEAR | VALUE |
      | R1     | ELC  | *    | 100   |
      | R1     | HEAT | *    | 100   |
    And VariableCost is
      | REGION | TECHNOLOGY | MODE_OF_OPERATION | YEAR | VALUE |
      | R1     | COAL       | 1                 | *    | 1     |
      | R1     | SOLAR      | 1                 | *    | 2     |
      | R1     | BOILER     | 1                 | *    | 1     |
    And RETagTechnology is
      | REGION | TECHNOLOGY | YEAR | VALUE |
      | R1     | SOLAR      | *    | 1     |
    When the model is solved
    Then ProductionByTechnologyAnnual is
      | REGION | TECHNOLOGY | FUEL | YEAR | VALUE |
      | R1     | COAL       | ELC  | *    | 60    |
      | R1     | SOLAR      | ELC  | *    | 40    |
      | R1     | BOILER     | HEAT | *    | 100   |
    And the objective is 234.2160175

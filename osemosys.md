OSeMOSYS 2017\_11\_08, the Open Source energy MOdelling SYStem, translated from the GNU MathProg file osemosys.txt. It finds the least discounted cost of meeting demand for fuels in every region, over the whole model period, by choosing new capacity, activity, storage and trade. Each constraint keeps the name it has in the MathProg file. Where the MathProg file computes a value from the coordinates of YEAR (`y - min(YEAR)`, `max(YEAR) - y`), the data supplies it as a parameter (YearsSinceStart, YearsUntilEnd), because an expression here cannot read a dimension's coordinates. A lag of one year, season or day type (`y-1`, `ls-1`, `ld-1`) is a shift of one position, so the file assumes, as OSeMOSYS does, that YEAR, SEASON and DAYTYPE are consecutive integers. The default values of OSeMOSYS parameters, such as -1 for "no limit", are data preparation: the data arrives with them filled in, as otoole writes it.

#### Sets

| Symbol | Meaning |
|---|---|
| $`\mathcal{R}`$ | index $`r`$ — `REGION` with $`\mathrm{TradeReverse}: \mathcal{R} \times \mathcal{E} \to \mathcal{R} \times \mathcal{E}`$ — regions, each balancing its own fuels |
| $`\mathcal{E}`$ | index $`e`$ — `_REGION` with $`\mathrm{TradeReverse}: \mathcal{R} \times \mathcal{E} \to \mathcal{R} \times \mathcal{E}`$ — the same labels as REGION, standing for the other end of a trade route — OSeMOSYS's `rr` |
| $`\mathcal{T}`$ | index $`t`$ — `TECHNOLOGY` — technologies, anything that converts, stores or delivers a fuel |
| $`\mathcal{I}`$ | index $`i`$ — `TIMESLICE` — the time slices a year is divided into |
| $`\mathcal{F}`$ | index $`f`$ — `FUEL` — fuels, energy carriers and energy services |
| $`\mathcal{M}`$ | index $`m`$ — `EMISSION` — emissions, any output tracked and penalised or capped |
| $`\mathcal{O}`$ | index $`o`$ — `MODE_OF_OPERATION` — the modes a technology runs in, each with its own input and output ratios |
| $`\mathcal{Y}`$ | index $`y`$ — `YEAR` — years of the model period, consecutive integers |
| $`\mathcal{S}`$ | index $`s`$ — `SEASON` — seasons, consecutive integers in their chronological order |
| $`\mathcal{D}`$ | index $`d`$ — `DAYTYPE` — day types, consecutive integers in their chronological order |
| $`\mathcal{A}`$ | index $`a`$ — `DAILYTIMEBRACKET` — the brackets a day is divided into, integers in their chronological order |
| $`\mathcal{G}`$ | index $`g`$ — `STORAGE` — storage facilities |

#### Parameters

| Symbol | Meaning |
|---|---|
| $`\mathrm{YearSplit}`$ | `YearSplit` over $`\mathcal{I} \times \mathcal{Y}`$ — the fraction of a year each time slice stands for |
| $`\mathrm{DiscountRate}`$ | `DiscountRate` over $`\mathcal{R}`$ — the region's discount rate |
| $`\mathrm{DiscountRateIdv}`$ | `DiscountRateIdv` over $`\mathcal{R} \times \mathcal{T}`$ — the technology's own discount rate, which only its capital recovery factor reads; DiscountRate where the data gives none |
| $`\mathrm{YearsSinceStart}`$ | `YearsSinceStart` over $`\mathcal{Y}`$ — years from the first year of the model period to this one, `y - min(YEAR)`, data prep |
| $`\mathrm{YearsUntilEnd}`$ | `YearsUntilEnd` over $`\mathcal{Y}`$ — years from this one to the end of the model period, this year included, `max(YEAR) - y + 1`, data prep. `YearsSinceStart + YearsUntilEnd` is the length of the model period in every year |
| $`\mathrm{OperationalLife}`$ | `OperationalLife` over $`\mathcal{R} \times \mathcal{T}`$ — the years a unit of new capacity stays in service |
| $`\mathrm{DiscountRateStorage}`$ | `DiscountRateStorage` over $`\mathcal{R} \times \mathcal{G}`$ — the discount rate of a storage facility |
| $`\mathrm{DaySplit}`$ | `DaySplit` over $`\mathcal{A} \times \mathcal{Y}`$ — the fraction of a year one daily time bracket stands for |
| $`\mathrm{Conversionls}`$ | `Conversionls` over $`\mathcal{I} \times \mathcal{S}`$ — one where the time slice falls in the season, zero elsewhere |
| $`\mathrm{Conversionld}`$ | `Conversionld` over $`\mathcal{I} \times \mathcal{D}`$ — one where the time slice falls on the day type, zero elsewhere |
| $`\mathrm{Conversionlh}`$ | `Conversionlh` over $`\mathcal{I} \times \mathcal{A}`$ — one where the time slice falls in the daily time bracket, zero elsewhere |
| $`\mathrm{DaysInDayType}`$ | `DaysInDayType` over $`\mathcal{S} \times \mathcal{D} \times \mathcal{Y}`$ — how many days of the day type one week of the season holds |
| $`\mathrm{TradeRoute}`$ | `TradeRoute` over $`\mathcal{R} \times \mathcal{E} \times \mathcal{F} \times \mathcal{Y}`$ — one where fuel may be traded from the region to the other, zero elsewhere |
| $`\mathrm{DepreciationMethod}`$ | `DepreciationMethod` over $`\mathcal{R}`$ — 1 for sinking-fund depreciation, 2 for straight-line depreciation |
| $`\mathrm{DailyTimeBracketCount}`$ | `DailyTimeBracketCount` (scalar) — how many daily time brackets there are, data prep — the width of a window that reaches back to the first bracket of the day from any other |
| $`\mathrm{SpecifiedAnnualDemand}`$ | `SpecifiedAnnualDemand` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — the annual demand for a fuel that has to be met in every time slice |
| $`\mathrm{SpecifiedDemandProfile}`$ | `SpecifiedDemandProfile` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{I} \times \mathcal{Y}`$ — the share of the annual specified demand falling in each time slice |
| $`\mathrm{AccumulatedAnnualDemand}`$ | `AccumulatedAnnualDemand` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — an annual demand for a fuel that may be met at any time of the year |
| $`\mathrm{CapacityToActivityUnit}`$ | `CapacityToActivityUnit` over $`\mathcal{R} \times \mathcal{T}`$ — the activity one unit of capacity yields when run for a whole year |
| $`\mathrm{CapacityFactor}`$ | `CapacityFactor` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{I} \times \mathcal{Y}`$ — the most a unit of capacity can run in a time slice, per unit |
| $`\mathrm{AvailabilityFactor}`$ | `AvailabilityFactor` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the share of the year capacity is available, after planned maintenance |
| $`\mathrm{ResidualCapacity}`$ | `ResidualCapacity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — capacity already installed before the model period, still in service |
| $`\mathrm{InputActivityRatio}`$ | `InputActivityRatio` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{F} \times \mathcal{O} \times \mathcal{Y}`$ — fuel used per unit of activity in a mode |
| $`\mathrm{OutputActivityRatio}`$ | `OutputActivityRatio` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{F} \times \mathcal{O} \times \mathcal{Y}`$ — fuel produced per unit of activity in a mode |
| $`\mathrm{CapitalCost}`$ | `CapitalCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the cost of one unit of new capacity |
| $`\mathrm{VariableCost}`$ | `VariableCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{O} \times \mathcal{Y}`$ — the cost of one unit of activity in a mode |
| $`\mathrm{FixedCost}`$ | `FixedCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the annual cost of one unit of installed capacity |
| $`\mathrm{TechnologyToStorage}`$ | `TechnologyToStorage` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{G} \times \mathcal{O}`$ — the share of a technology's activity in a mode that charges the storage |
| $`\mathrm{TechnologyFromStorage}`$ | `TechnologyFromStorage` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{G} \times \mathcal{O}`$ — the share of a technology's activity in a mode that discharges the storage |
| $`\mathrm{StorageLevelStart}`$ | `StorageLevelStart` over $`\mathcal{R} \times \mathcal{G}`$ — the storage level at the start of the first year |
| $`\mathrm{StorageMaxChargeRate}`$ | `StorageMaxChargeRate` over $`\mathcal{R} \times \mathcal{G}`$ — the highest rate the storage charges at |
| $`\mathrm{StorageMaxDischargeRate}`$ | `StorageMaxDischargeRate` over $`\mathcal{R} \times \mathcal{G}`$ — the highest rate the storage discharges at |
| $`\mathrm{MinStorageCharge}`$ | `MinStorageCharge` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the lowest storage level, as a share of the storage's capacity |
| $`\mathrm{OperationalLifeStorage}`$ | `OperationalLifeStorage` over $`\mathcal{R} \times \mathcal{G}`$ — the years new storage capacity stays in service |
| $`\mathrm{CapitalCostStorage}`$ | `CapitalCostStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the cost of one unit of new storage capacity |
| $`\mathrm{ResidualStorageCapacity}`$ | `ResidualStorageCapacity` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — storage capacity already installed before the model period |
| $`\mathrm{CapacityOfOneTechnologyUnit}`$ | `CapacityOfOneTechnologyUnit` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the size of one unit where capacity is built in whole units; zero where it is continuous |
| $`\mathrm{TotalAnnualMaxCapacity}`$ | `TotalAnnualMaxCapacity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the most capacity a technology may have in a year; -1 for no limit |
| $`\mathrm{TotalAnnualMinCapacity}`$ | `TotalAnnualMinCapacity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the least capacity a technology must have in a year |
| $`\mathrm{TotalAnnualMaxCapacityInvestment}`$ | `TotalAnnualMaxCapacityInvestment` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the most new capacity a technology may gain in a year; -1 for no limit |
| $`\mathrm{TotalAnnualMinCapacityInvestment}`$ | `TotalAnnualMinCapacityInvestment` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the least new capacity a technology must gain in a year |
| $`\mathrm{TotalTechnologyAnnualActivityUpperLimit}`$ | `TotalTechnologyAnnualActivityUpperLimit` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the most activity a technology may have in a year; -1 for no limit |
| $`\mathrm{TotalTechnologyAnnualActivityLowerLimit}`$ | `TotalTechnologyAnnualActivityLowerLimit` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the least activity a technology must have in a year |
| $`\mathrm{TotalTechnologyModelPeriodActivityUpperLimit}`$ | `TotalTechnologyModelPeriodActivityUpperLimit` over $`\mathcal{R} \times \mathcal{T}`$ — the most activity a technology may have over the model period; -1 for no limit |
| $`\mathrm{TotalTechnologyModelPeriodActivityLowerLimit}`$ | `TotalTechnologyModelPeriodActivityLowerLimit` over $`\mathcal{R} \times \mathcal{T}`$ — the least activity a technology must have over the model period |
| $`\mathrm{ReserveMarginTagTechnology}`$ | `ReserveMarginTagTechnology` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the share of a technology's capacity that counts towards the reserve margin |
| $`\mathrm{ReserveMarginTagFuel}`$ | `ReserveMarginTagFuel` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — one where production of the fuel needs a reserve margin, zero elsewhere |
| $`\mathrm{ReserveMargin}`$ | `ReserveMargin` over $`\mathcal{R} \times \mathcal{Y}`$ — the capacity that has to stand behind peak production, as a multiple of it |
| $`\mathrm{RETagTechnology}`$ | `RETagTechnology` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — one where the technology is renewable, zero elsewhere |
| $`\mathrm{RETagFuel}`$ | `RETagFuel` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — one where the fuel counts towards the renewable target, zero elsewhere |
| $`\mathrm{REMinProductionTarget}`$ | `REMinProductionTarget` over $`\mathcal{R} \times \mathcal{Y}`$ — the least share of target-fuel production that has to be renewable |
| $`\mathrm{EmissionActivityRatio}`$ | `EmissionActivityRatio` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{M} \times \mathcal{O} \times \mathcal{Y}`$ — emission released per unit of activity in a mode |
| $`\mathrm{EmissionsPenalty}`$ | `EmissionsPenalty` over $`\mathcal{R} \times \mathcal{M} \times \mathcal{Y}`$ — the cost of one unit of emission |
| $`\mathrm{AnnualExogenousEmission}`$ | `AnnualExogenousEmission` over $`\mathcal{R} \times \mathcal{M} \times \mathcal{Y}`$ — emission released in a year by anything outside the model |
| $`\mathrm{AnnualEmissionLimit}`$ | `AnnualEmissionLimit` over $`\mathcal{R} \times \mathcal{M} \times \mathcal{Y}`$ — the most emission a year may release; -1 for no limit |
| $`\mathrm{ModelPeriodExogenousEmission}`$ | `ModelPeriodExogenousEmission` over $`\mathcal{R} \times \mathcal{M}`$ — emission released over the model period by anything outside the model |
| $`\mathrm{ModelPeriodEmissionLimit}`$ | `ModelPeriodEmissionLimit` over $`\mathcal{R} \times \mathcal{M}`$ — the most emission the model period may release; -1 for no limit |

#### Variables

| Symbol | Meaning |
|---|---|
| $`\mathit{RateOfDemand}`$ | `RateOfDemand` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a fuel is demanded at in a time slice |
| $`\mathit{Demand}`$ | `Demand` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel demanded in a time slice |
| $`\mathit{RateOfStorageCharge}`$ | `RateOfStorageCharge` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{A} \times \mathcal{Y}`$ — the rate the storage charges at in a daily time bracket |
| $`\mathit{RateOfStorageDischarge}`$ | `RateOfStorageDischarge` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{A} \times \mathcal{Y}`$ — the rate the storage discharges at in a daily time bracket |
| $`\mathit{NetChargeWithinYear}`$ | `NetChargeWithinYear` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{A} \times \mathcal{Y}`$ — the net charge into the storage in a daily time bracket, over the year |
| $`\mathit{NetChargeWithinDay}`$ | `NetChargeWithinDay` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{A} \times \mathcal{Y}`$ — the net charge into the storage in a daily time bracket, over one day |
| $`\mathit{StorageLevelYearStart}`$ | `StorageLevelYearStart` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the storage level at the start of the year |
| $`\mathit{StorageLevelYearFinish}`$ | `StorageLevelYearFinish` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the storage level at the end of the year |
| $`\mathit{StorageLevelSeasonStart}`$ | `StorageLevelSeasonStart` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{Y}`$ — the storage level at the start of the season |
| $`\mathit{StorageLevelDayTypeStart}`$ | `StorageLevelDayTypeStart` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{Y}`$ — the storage level at the start of the first day of the day type |
| $`\mathit{StorageLevelDayTypeFinish}`$ | `StorageLevelDayTypeFinish` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{Y}`$ — the storage level at the end of the last day of the day type |
| $`\mathit{StorageLowerLimit}`$ | `StorageLowerLimit` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the lowest level the storage may hold |
| $`\mathit{StorageUpperLimit}`$ | `StorageUpperLimit` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the highest level the storage may hold, its capacity |
| $`\mathit{AccumulatedNewStorageCapacity}`$ | `AccumulatedNewStorageCapacity` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — new storage capacity built in the model period and still in service |
| $`\mathit{NewStorageCapacity}`$ | `NewStorageCapacity` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — storage capacity built in the year |
| $`\mathit{CapitalInvestmentStorage}`$ | `CapitalInvestmentStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the undiscounted cost of the storage capacity built in the year |
| $`\mathit{DiscountedCapitalInvestmentStorage}`$ | `DiscountedCapitalInvestmentStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the cost of the storage capacity built in the year, discounted to the first year |
| $`\mathit{SalvageValueStorage}`$ | `SalvageValueStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — what the storage capacity built in the year is still worth at the end of the model period |
| $`\mathit{DiscountedSalvageValueStorage}`$ | `DiscountedSalvageValueStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the salvage value of the storage, discounted to the first year |
| $`\mathit{TotalDiscountedStorageCost}`$ | `TotalDiscountedStorageCost` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the discounted cost of the storage, less its discounted salvage value |
| $`\mathit{NumberOfNewTechnologyUnits}`$ | `NumberOfNewTechnologyUnits` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — how many whole units are built in the year; it exists only where capacity comes in units, since nothing reads it anywhere else |
| $`\mathit{NewCapacity}`$ | `NewCapacity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — capacity built in the year |
| $`\mathit{AccumulatedNewCapacity}`$ | `AccumulatedNewCapacity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — new capacity built in the model period and still in service |
| $`\mathit{TotalCapacityAnnual}`$ | `TotalCapacityAnnual` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — all capacity in service in the year |
| $`\mathit{RateOfActivity}`$ | `RateOfActivity` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{O} \times \mathcal{Y}`$ — the rate a technology runs at in a mode, in a time slice |
| $`\mathit{RateOfTotalActivity}`$ | `RateOfTotalActivity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{I} \times \mathcal{Y}`$ — the rate a technology runs at in a time slice, over every mode |
| $`\mathit{TotalTechnologyAnnualActivity}`$ | `TotalTechnologyAnnualActivity` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — a technology's activity over the year |
| $`\mathit{TotalAnnualTechnologyActivityByMode}`$ | `TotalAnnualTechnologyActivityByMode` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{O} \times \mathcal{Y}`$ — a technology's activity in a mode over the year |
| $`\mathit{TotalTechnologyModelPeriodActivity}`$ | `TotalTechnologyModelPeriodActivity` over $`\mathcal{R} \times \mathcal{T}`$ — a technology's activity over the model period |
| $`\mathit{RateOfProductionByTechnologyByMode}`$ | `RateOfProductionByTechnologyByMode` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{O} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a technology produces a fuel at in a mode; it exists only where the mode produces the fuel, which is where MathProg's sum over modes reads it |
| $`\mathit{RateOfProductionByTechnology}`$ | `RateOfProductionByTechnology` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a technology produces a fuel at, over every mode |
| $`\mathit{ProductionByTechnology}`$ | `ProductionByTechnology` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel a technology produces in a time slice |
| $`\mathit{ProductionByTechnologyAnnual}`$ | `ProductionByTechnologyAnnual` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel a technology produces over the year |
| $`\mathit{RateOfProduction}`$ | `RateOfProduction` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a fuel is produced at, over every technology |
| $`\mathit{Production}`$ | `Production` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel produced in a time slice |
| $`\mathit{RateOfUseByTechnologyByMode}`$ | `RateOfUseByTechnologyByMode` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{O} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a technology uses a fuel at in a mode; it exists only where the mode uses the fuel, which is where MathProg's sum over modes reads it |
| $`\mathit{RateOfUseByTechnology}`$ | `RateOfUseByTechnology` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a technology uses a fuel at, over every mode |
| $`\mathit{UseByTechnologyAnnual}`$ | `UseByTechnologyAnnual` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel a technology uses over the year |
| $`\mathit{RateOfUse}`$ | `RateOfUse` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the rate a fuel is used at, over every technology |
| $`\mathit{UseByTechnology}`$ | `UseByTechnology` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{T} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel a technology uses in a time slice |
| $`\mathit{Use}`$ | `Use` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel used in a time slice |
| $`\mathit{Trade}`$ | `Trade` over $`\mathcal{R} \times \mathcal{E} \times \mathcal{I} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel sent from the region to the other in a time slice; negative where it is received |
| $`\mathit{TradeAnnual}`$ | `TradeAnnual` over $`\mathcal{R} \times \mathcal{E} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel sent from the region to the other over the year |
| $`\mathit{ProductionAnnual}`$ | `ProductionAnnual` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel produced over the year |
| $`\mathit{UseAnnual}`$ | `UseAnnual` over $`\mathcal{R} \times \mathcal{F} \times \mathcal{Y}`$ — the fuel used over the year |
| $`\mathit{CapitalInvestment}`$ | `CapitalInvestment` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the undiscounted cost of the capacity built in the year |
| $`\mathit{DiscountedCapitalInvestment}`$ | `DiscountedCapitalInvestment` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the cost of the capacity built in the year, discounted to the first year |
| $`\mathit{SalvageValue}`$ | `SalvageValue` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — what the capacity built in the year is still worth at the end of the model period |
| $`\mathit{DiscountedSalvageValue}`$ | `DiscountedSalvageValue` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the salvage value, discounted to the first year |
| $`\mathit{OperatingCost}`$ | `OperatingCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the undiscounted fixed and variable operating cost of the year |
| $`\mathit{DiscountedOperatingCost}`$ | `DiscountedOperatingCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the operating cost of the year, discounted to the first year from mid-year |
| $`\mathit{AnnualVariableOperatingCost}`$ | `AnnualVariableOperatingCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the undiscounted variable operating cost of the year |
| $`\mathit{AnnualFixedOperatingCost}`$ | `AnnualFixedOperatingCost` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the undiscounted fixed operating cost of the year |
| $`\mathit{TotalDiscountedCostByTechnology}`$ | `TotalDiscountedCostByTechnology` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — every discounted cost of a technology in the year, less its discounted salvage value |
| $`\mathit{TotalDiscountedCost}`$ | `TotalDiscountedCost` over $`\mathcal{R} \times \mathcal{Y}`$ — every discounted cost of the region in the year |
| $`\mathit{ModelPeriodCostByRegion}`$ | `ModelPeriodCostByRegion` over $`\mathcal{R}`$ — every discounted cost of the region over the model period |
| $`\mathit{TotalCapacityInReserveMargin}`$ | `TotalCapacityInReserveMargin` over $`\mathcal{R} \times \mathcal{Y}`$ — the capacity that counts towards the reserve margin, in activity units |
| $`\mathit{DemandNeedingReserveMargin}`$ | `DemandNeedingReserveMargin` over $`\mathcal{R} \times \mathcal{I} \times \mathcal{Y}`$ — the rate of production that needs a reserve margin, in a time slice |
| $`\mathit{TotalREProductionAnnual}`$ | `TotalREProductionAnnual` over $`\mathcal{R} \times \mathcal{Y}`$ — the fuel renewable technologies produce over the year |
| $`\mathit{RETotalProductionOfTargetFuelAnnual}`$ | `RETotalProductionOfTargetFuelAnnual` over $`\mathcal{R} \times \mathcal{Y}`$ — the production of the fuels the renewable target counts, over the year |
| $`\mathit{AnnualTechnologyEmissionByMode}`$ | `AnnualTechnologyEmissionByMode` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{M} \times \mathcal{O} \times \mathcal{Y}`$ — the emission a technology releases in a mode over the year |
| $`\mathit{AnnualTechnologyEmission}`$ | `AnnualTechnologyEmission` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{M} \times \mathcal{Y}`$ — the emission a technology releases over the year |
| $`\mathit{AnnualTechnologyEmissionPenaltyByEmission}`$ | `AnnualTechnologyEmissionPenaltyByEmission` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{M} \times \mathcal{Y}`$ — the undiscounted penalty on one emission of a technology in the year |
| $`\mathit{AnnualTechnologyEmissionsPenalty}`$ | `AnnualTechnologyEmissionsPenalty` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the undiscounted penalty on every emission of a technology in the year |
| $`\mathit{DiscountedTechnologyEmissionsPenalty}`$ | `DiscountedTechnologyEmissionsPenalty` over $`\mathcal{R} \times \mathcal{T} \times \mathcal{Y}`$ — the emissions penalty of the year, discounted to the first year from mid-year |
| $`\mathit{AnnualEmissions}`$ | `AnnualEmissions` over $`\mathcal{R} \times \mathcal{M} \times \mathcal{Y}`$ — the emission the region releases over the year |
| $`\mathit{ModelPeriodEmissions}`$ | `ModelPeriodEmissions` over $`\mathcal{R} \times \mathcal{M}`$ — the emission the region releases over the model period, exogenous emission included |

#### Definitions

| Symbol | Meaning |
|---|---|
| $`\mathrm{DiscountFactor}`$ | `DiscountFactor` over $`\mathcal{R} \times \mathcal{Y}`$ — what one unit of cost at the start of the year is worth in the first year |
| $`\mathrm{DiscountFactorMid}`$ | `DiscountFactorMid` over $`\mathcal{R} \times \mathcal{Y}`$ — what one unit of cost in the middle of the year is worth in the first year |
| $`\mathrm{CapitalRecoveryFactor}`$ | `CapitalRecoveryFactor` over $`\mathcal{R} \times \mathcal{T}`$ — the share of a technology's capital cost paid each year over its operational life, at its own discount rate DiscountRateIdv |
| $`\mathrm{PvAnnuity}`$ | `PvAnnuity` over $`\mathcal{R} \times \mathcal{T}`$ — the present value of an annuity over a technology's operational life |
| $`\mathrm{DiscountFactorStorage}`$ | `DiscountFactorStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — what one unit of storage cost at the start of the year is worth in the first year |
| $`\mathrm{DiscountFactorMidStorage}`$ | `DiscountFactorMidStorage` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — what one unit of storage cost in the middle of the year is worth in the first year; declared by OSeMOSYS and read by none of its constraints |
| $`\mathit{StorageLevelYearStartCarried}`$ | `StorageLevelYearStartCarried` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the storage level a year starts with — the initial level, or where the previous year ended |
| $`\mathit{StorageLevelYearFinishCarried}`$ | `StorageLevelYearFinishCarried` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{Y}`$ — the storage level a year ends with — where the next year starts, or the last year's own balance |
| $`\mathit{StorageLevelSeasonStartCarried}`$ | `StorageLevelSeasonStartCarried` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{Y}`$ — the storage level a season starts with — where the year starts, or where the previous season ended |
| $`\mathit{StorageLevelDayTypeStartCarried}`$ | `StorageLevelDayTypeStartCarried` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{Y}`$ — the storage level a day type starts with — where the season starts, or where the previous day type ended |
| $`\mathit{StorageLevelDayTypeFinishCarried}`$ | `StorageLevelDayTypeFinishCarried` over $`\mathcal{R} \times \mathcal{G} \times \mathcal{S} \times \mathcal{D} \times \mathcal{Y}`$ — the storage level a day type ends with — where the year ends after the last day type of the last season, where the next season starts after the last day type of any other, and otherwise the next day type's finish less what that day type charges |

Upright is what the data supplies — a parameter such as $`\mathrm{YearSplit}`$, a coordinate map, a label — and italic is what the solver chooses, such as $`\mathit{RateOfDemand}`$. An index is italic too, being what a quantifier chooses, and a set is script.

$`\mathrm{pos}(t)`$ denotes where index $`t`$ sits along its dimension's own order — the order `shift` steps along, not the order labels sort in — counted from $`0`$. The index itself stays the coordinate, so $`t`$ compares against labels and $`\mathrm{pos}(t)`$ against positions.

$`\lvert \mathcal{T} \rvert`$ denotes the size of the set being counted along, and a position counted from the end prints against it — $`\lvert \mathcal{T} \rvert - 1`$ is the last position, one less than the size because the first is $`0`$.

#### Objective

```math
\min \sum_{r \in \mathcal{R},\ y \in \mathcal{Y}} \mathit{TotalDiscountedCost}_{r,y}
```

#### Subject to

**`EQ_SpecifiedDemand`**

```math
\frac{\mathrm{SpecifiedAnnualDemand}_{r,f,y} \cdot \mathrm{SpecifiedDemandProfile}_{r,f,i,y}}{\mathrm{YearSplit}_{i,y}} = \mathit{RateOfDemand}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \mathrm{SpecifiedAnnualDemand}_{r,f,y} \neq 0
```

**`CAa1_TotalNewCapacity`**

```math
\mathit{AccumulatedNewCapacity}_{r,t,y} = \sum_{y' \in \mathcal{Y} \,:\, 0 \le y - y' < \mathrm{OperationalLife}} \mathit{NewCapacity}_{r,t,y'} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`CAa2_TotalAnnualCapacity`**

```math
\mathit{AccumulatedNewCapacity}_{r,t,y} + \mathrm{ResidualCapacity}_{r,t,y} = \mathit{TotalCapacityAnnual}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`CAa3_TotalActivityOfEachTechnology`**

```math
\sum_{o \in \mathcal{O}} \mathit{RateOfActivity}_{r,i,t,o,y} = \mathit{RateOfTotalActivity}_{r,t,i,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ i \in \mathcal{I},\ y \in \mathcal{Y}
```

**`CAa4_Constraint_Capacity`**

```math
\mathit{RateOfTotalActivity}_{r,t,i,y} \le \mathit{TotalCapacityAnnual}_{r,t,y} \cdot \mathrm{CapacityFactor}_{r,t,i,y} \cdot \mathrm{CapacityToActivityUnit}_{r,t} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`CAa5_TotalNewCapacity`**

```math
\mathrm{CapacityOfOneTechnologyUnit}_{r,t,y} \cdot \mathit{NumberOfNewTechnologyUnits}_{r,t,y} = \mathit{NewCapacity}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{CapacityOfOneTechnologyUnit}_{r,t,y} \neq 0
```

**`CAb1_PlannedMaintenance`**

```math
\sum_{i \in \mathcal{I}} \mathit{RateOfTotalActivity}_{r,t,i,y} \cdot \mathrm{YearSplit}_{i,y} \le \left( \sum_{i \in \mathcal{I}} \mathit{TotalCapacityAnnual}_{r,t,y} \cdot \mathrm{CapacityFactor}_{r,t,i,y} \cdot \mathrm{YearSplit}_{i,y} \right) \cdot \mathrm{AvailabilityFactor}_{r,t,y} \cdot \mathrm{CapacityToActivityUnit}_{r,t} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{AvailabilityFactor}_{r,t,y} < 1
```

**`EBa1_RateOfFuelProduction1`**

```math
\mathit{RateOfActivity}_{r,i,t,o,y} \cdot \mathrm{OutputActivityRatio}_{r,t,f,o,y} = \mathit{RateOfProductionByTechnologyByMode}_{r,i,t,o,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ t \in \mathcal{T},\ o \in \mathcal{O},\ y \in \mathcal{Y} \,:\, \mathrm{OutputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa2_RateOfFuelProduction2`**

```math
\sum_{o \in \mathcal{O}} \mathit{RateOfProductionByTechnologyByMode}_{r,i,t,o,f,y} = \mathit{RateOfProductionByTechnology}_{r,i,t,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`EBa3_RateOfFuelProduction3`**

```math
\sum_{t \in \mathcal{T}} \mathit{RateOfProductionByTechnology}_{r,i,t,f,y} = \mathit{RateOfProduction}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathrm{OutputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa4_RateOfFuelUse1`**

```math
\mathit{RateOfActivity}_{r,i,t,o,y} \cdot \mathrm{InputActivityRatio}_{r,t,f,o,y} = \mathit{RateOfUseByTechnologyByMode}_{r,i,t,o,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ t \in \mathcal{T},\ o \in \mathcal{O},\ y \in \mathcal{Y} \,:\, \mathrm{InputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa5_RateOfFuelUse2`**

```math
\sum_{o \in \mathcal{O}} \mathit{RateOfUseByTechnologyByMode}_{r,i,t,o,f,y} = \mathit{RateOfUseByTechnology}_{r,i,t,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \mathrm{InputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa6_RateOfFuelUse3`**

```math
\sum_{t \in \mathcal{T}} \mathit{RateOfUseByTechnology}_{r,i,t,f,y} = \mathit{RateOfUse}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathrm{InputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa7_EnergyBalanceEachTS1`**

```math
\mathit{RateOfProduction}_{r,i,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{Production}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathrm{OutputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa8_EnergyBalanceEachTS2`**

```math
\mathit{RateOfUse}_{r,i,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{Use}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathrm{InputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`EBa9_EnergyBalanceEachTS3`**

```math
\mathit{RateOfDemand}_{r,i,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{Demand}_{r,i,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \mathrm{SpecifiedAnnualDemand}_{r,f,y} \neq 0
```

**`EBa10_EnergyBalanceEachTS4`**

```math
\mathit{Trade}_{r,e,i,f,y} = -\mathit{Trade}_{\mathrm{TradeReverse.reverse\_region}(r,\ e),\mathrm{TradeReverse.reverse\_partner}(r,\ e),i,f,y} \qquad \forall\, r \in \mathcal{R},\ e \in \mathcal{E},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \mathrm{TradeRoute}_{r,e,f,y} \neq 0
```

**`EBa11_EnergyBalanceEachTS5`**

```math
\mathit{Production}_{r,i,f,y} \ge \mathit{Demand}_{r,i,f,y} + \mathit{Use}_{r,i,f,y} + \sum_{e \in \mathcal{E}} \mathit{Trade}_{r,e,i,f,y} \cdot \mathrm{TradeRoute}_{r,e,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`EBb1_EnergyBalanceEachYear1`**

```math
\sum_{i \in \mathcal{I}} \mathit{Production}_{r,i,f,y} = \mathit{ProductionAnnual}_{r,f,y} \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`EBb2_EnergyBalanceEachYear2`**

```math
\sum_{i \in \mathcal{I}} \mathit{Use}_{r,i,f,y} = \mathit{UseAnnual}_{r,f,y} \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`EBb3_EnergyBalanceEachYear3`**

```math
\sum_{i \in \mathcal{I}} \mathit{Trade}_{r,e,i,f,y} = \mathit{TradeAnnual}_{r,e,f,y} \qquad \forall\, r \in \mathcal{R},\ e \in \mathcal{E},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`EBb4_EnergyBalanceEachYear4`**

```math
\mathit{ProductionAnnual}_{r,f,y} \ge \mathit{UseAnnual}_{r,f,y} + \sum_{e \in \mathcal{E}} \mathit{TradeAnnual}_{r,e,f,y} \cdot \mathrm{TradeRoute}_{r,e,f,y} + \mathrm{AccumulatedAnnualDemand}_{r,f,y} \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Acc1_FuelProductionByTechnology`**

```math
\mathit{RateOfProductionByTechnology}_{r,i,t,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{ProductionByTechnology}_{r,i,t,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Acc2_FuelUseByTechnology`**

```math
\mathit{RateOfUseByTechnology}_{r,i,t,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{UseByTechnology}_{r,i,t,f,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Acc3_AverageAnnualRateOfActivity`**

```math
\sum_{i \in \mathcal{I}} \mathit{RateOfActivity}_{r,i,t,o,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{TotalAnnualTechnologyActivityByMode}_{r,t,o,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ o \in \mathcal{O},\ y \in \mathcal{Y}
```

**`Acc4_ModelPeriodCostByRegion`**

```math
\sum_{y \in \mathcal{Y}} \mathit{TotalDiscountedCost}_{r,y} = \mathit{ModelPeriodCostByRegion}_{r} \qquad \forall\, r \in \mathcal{R}
```

**`S1_RateOfStorageCharge`**

```math
\sum_{i \in \mathcal{I}} \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathit{RateOfActivity}_{r,i,t,o,y} \cdot \mathrm{TechnologyToStorage}_{r,t,g,o} \cdot \mathrm{Conversionls}_{i,s} \cdot \mathrm{Conversionld}_{i,d} \cdot \mathrm{Conversionlh}_{i,a} = \mathit{RateOfStorageCharge}_{r,g,s,d,a,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`S2_RateOfStorageDischarge`**

```math
\sum_{i \in \mathcal{I}} \sum_{o \in \mathcal{O}} \sum_{t \in \mathcal{T}} \mathit{RateOfActivity}_{r,i,t,o,y} \cdot \mathrm{TechnologyFromStorage}_{r,t,g,o} \cdot \mathrm{Conversionls}_{i,s} \cdot \mathrm{Conversionld}_{i,d} \cdot \mathrm{Conversionlh}_{i,a} = \mathit{RateOfStorageDischarge}_{r,g,s,d,a,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`S3_NetChargeWithinYear`**

```math
\sum_{i \in \mathcal{I}} \left( \mathit{RateOfStorageCharge}_{r,g,s,d,a,y} - \mathit{RateOfStorageDischarge}_{r,g,s,d,a,y} \right) \cdot \mathrm{YearSplit}_{i,y} \cdot \mathrm{Conversionls}_{i,s} \cdot \mathrm{Conversionld}_{i,d} \cdot \mathrm{Conversionlh}_{i,a} = \mathit{NetChargeWithinYear}_{r,g,s,d,a,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`S4_NetChargeWithinDay`**

```math
\left( \mathit{RateOfStorageCharge}_{r,g,s,d,a,y} - \mathit{RateOfStorageDischarge}_{r,g,s,d,a,y} \right) \cdot \mathrm{DaySplit}_{a,y} = \mathit{NetChargeWithinDay}_{r,g,s,d,a,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`S5_and_S6_StorageLevelYearStart`**

```math
\mathit{StorageLevelYearStartCarried}_{r,g,y} = \mathit{StorageLevelYearStart}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`S7_and_S8_StorageLevelYearFinish`**

```math
\mathit{StorageLevelYearFinishCarried}_{r,g,y} = \mathit{StorageLevelYearFinish}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`S9_and_S10_StorageLevelSeasonStart`**

```math
\mathit{StorageLevelSeasonStartCarried}_{r,g,s,y} = \mathit{StorageLevelSeasonStart}_{r,g,s,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ y \in \mathcal{Y}
```

**`S11_and_S12_StorageLevelDayTypeStart`**

```math
\mathit{StorageLevelDayTypeStartCarried}_{r,g,s,d,y} = \mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

**`S13_and_S14_and_S15_StorageLevelDayTypeFinish`**

```math
\mathit{StorageLevelDayTypeFinishCarried}_{r,g,s,d,y} = \mathit{StorageLevelDayTypeFinish}_{r,g,s,d,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

**`SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint`**

```math
0 \le \mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} + \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \mathit{NetChargeWithinDay}_{r,g,s,d,a,y} - \mathit{StorageLowerLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint`**

```math
\mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} + \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \mathit{NetChargeWithinDay}_{r,g,s,d,a,y} - \mathit{StorageUpperLimit}_{r,g,y} \le 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint`**

```math
0 \le \mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} - \left( \sum_{a' \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d - 1,a',y} - \left( \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d - 1,a',y} \right) \right) - \mathit{StorageLowerLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y} \,:\, \mathrm{pos}(d) > 0
```

**`SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint`**

```math
\mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} - \left( \sum_{a' \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d - 1,a',y} - \left( \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d - 1,a',y} \right) \right) - \mathit{StorageUpperLimit}_{r,g,y} \le 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y} \,:\, \mathrm{pos}(d) > 0
```

**`SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint`**

```math
0 \le \mathit{StorageLevelDayTypeFinish}_{r,g,s,d,y} - \left( \sum_{a' \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \left( \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} \right) \right) - \mathit{StorageLowerLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint`**

```math
\mathit{StorageLevelDayTypeFinish}_{r,g,s,d,y} - \left( \sum_{a' \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \left( \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} \right) \right) - \mathit{StorageUpperLimit}_{r,g,y} \le 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint`**

```math
0 \le \mathit{StorageLevelDayTypeFinish}_{r,g,s,d - 1,y} + \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \mathit{NetChargeWithinDay}_{r,g,s,d,a,y} - \mathit{StorageLowerLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y} \,:\, \mathrm{pos}(d) > 0
```

**`SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint`**

```math
\mathit{StorageLevelDayTypeFinish}_{r,g,s,d - 1,y} + \sum_{a' \in \mathcal{A} \,:\, 0 \le a - a' < \mathrm{DailyTimeBracketCount}} \mathit{NetChargeWithinDay}_{r,g,s,d,a',y} - \mathit{NetChargeWithinDay}_{r,g,s,d,a,y} - \mathit{StorageUpperLimit}_{r,g,y} \le 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y} \,:\, \mathrm{pos}(d) > 0
```

**`SC5_MaxChargeConstraint`**

```math
\mathit{RateOfStorageCharge}_{r,g,s,d,a,y} \le \mathrm{StorageMaxChargeRate}_{r,g} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SC6_MaxDischargeConstraint`**

```math
\mathit{RateOfStorageDischarge}_{r,g,s,d,a,y} \le \mathrm{StorageMaxDischargeRate}_{r,g} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`SI1_StorageUpperLimit`**

```math
\mathit{AccumulatedNewStorageCapacity}_{r,g,y} + \mathrm{ResidualStorageCapacity}_{r,g,y} = \mathit{StorageUpperLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI2_StorageLowerLimit`**

```math
\mathrm{MinStorageCharge}_{r,g,y} \cdot \mathit{StorageUpperLimit}_{r,g,y} = \mathit{StorageLowerLimit}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI3_TotalNewStorage`**

```math
\sum_{y' \in \mathcal{Y} \,:\, 0 \le y - y' < \mathrm{OperationalLifeStorage}} \mathit{NewStorageCapacity}_{r,g,y'} = \mathit{AccumulatedNewStorageCapacity}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI4_UndiscountedCapitalInvestmentStorage`**

```math
\mathrm{CapitalCostStorage}_{r,g,y} \cdot \mathit{NewStorageCapacity}_{r,g,y} = \mathit{CapitalInvestmentStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI5_DiscountingCapitalInvestmentStorage`**

```math
\frac{\mathit{CapitalInvestmentStorage}_{r,g,y}}{\mathrm{DiscountFactorStorage}_{r,g,y}} = \mathit{DiscountedCapitalInvestmentStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI6_SalvageValueStorageAtEndOfPeriod1`**

```math
0 = \mathit{SalvageValueStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y} \,:\, \mathrm{OperationalLifeStorage}_{r,g} \le \mathrm{YearsUntilEnd}_{y}
```

**`SI7_SalvageValueStorageAtEndOfPeriod2`**

```math
\mathit{CapitalInvestmentStorage}_{r,g,y} \cdot \left( 1 - \frac{\mathrm{YearsUntilEnd}_{y}}{\mathrm{OperationalLifeStorage}_{r,g}} \right) = \mathit{SalvageValueStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y} \,:\, \mathrm{DepreciationMethod}_{r} = 1 \wedge \mathrm{OperationalLifeStorage}_{r,g} > \mathrm{YearsUntilEnd}_{y} \wedge \mathrm{DiscountRateStorage}_{r,g} = 0 \vee \mathrm{DepreciationMethod}_{r} = 2 \wedge \mathrm{OperationalLifeStorage}_{r,g} > \mathrm{YearsUntilEnd}_{y}
```

**`SI8_SalvageValueStorageAtEndOfPeriod3`**

```math
\mathit{CapitalInvestmentStorage}_{r,g,y} \cdot \left( 1 - \frac{\left( 1 + \mathrm{DiscountRateStorage}_{r,g} \right)^{\mathrm{YearsUntilEnd}_{y}} - 1}{\left( 1 + \mathrm{DiscountRateStorage}_{r,g} \right)^{\mathrm{OperationalLifeStorage}_{r,g}} - 1} \right) = \mathit{SalvageValueStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y} \,:\, \mathrm{DepreciationMethod}_{r} = 1 \wedge \mathrm{OperationalLifeStorage}_{r,g} > \mathrm{YearsUntilEnd}_{y} \wedge \mathrm{DiscountRateStorage}_{r,g} > 0
```

**`SI9_SalvageValueStorageDiscountedToStartYear`**

```math
\frac{\mathit{SalvageValueStorage}_{r,g,y}}{\left( 1 + \mathrm{DiscountRateStorage}_{r,g} \right)^{\mathrm{YearsSinceStart}_{y} + \mathrm{YearsUntilEnd}_{y}}} = \mathit{DiscountedSalvageValueStorage}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SI10_TotalDiscountedCostByStorage`**

```math
\mathit{DiscountedCapitalInvestmentStorage}_{r,g,y} - \mathit{DiscountedSalvageValueStorage}_{r,g,y} = \mathit{TotalDiscountedStorageCost}_{r,g,y} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`CC1_UndiscountedCapitalInvestment`**

```math
\mathrm{CapitalCost}_{r,t,y} \cdot \mathit{NewCapacity}_{r,t,y} \cdot \mathrm{CapitalRecoveryFactor}_{r,t} \cdot \mathrm{PvAnnuity}_{r,t} = \mathit{CapitalInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`CC2_DiscountingCapitalInvestment`**

```math
\frac{\mathit{CapitalInvestment}_{r,t,y}}{\mathrm{DiscountFactor}_{r,y}} = \mathit{DiscountedCapitalInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`SV1_SalvageValueAtEndOfPeriod1`**

```math
\mathit{SalvageValue}_{r,t,y} = \mathrm{CapitalCost}_{r,t,y} \cdot \mathit{NewCapacity}_{r,t,y} \cdot \mathrm{CapitalRecoveryFactor}_{r,t} \cdot \mathrm{PvAnnuity}_{r,t} \cdot \left( 1 - \frac{\left( 1 + \mathrm{DiscountRate}_{r} \right)^{\mathrm{YearsUntilEnd}_{y}} - 1}{\left( 1 + \mathrm{DiscountRate}_{r} \right)^{\mathrm{OperationalLife}_{r,t}} - 1} \right) \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{DepreciationMethod}_{r} = 1 \wedge \mathrm{OperationalLife}_{r,t} > \mathrm{YearsUntilEnd}_{y} \wedge \mathrm{DiscountRate}_{r} > 0
```

**`SV2_SalvageValueAtEndOfPeriod2`**

```math
\mathit{SalvageValue}_{r,t,y} = \mathrm{CapitalCost}_{r,t,y} \cdot \mathit{NewCapacity}_{r,t,y} \cdot \mathrm{CapitalRecoveryFactor}_{r,t} \cdot \mathrm{PvAnnuity}_{r,t} \cdot \left( 1 - \frac{\mathrm{YearsUntilEnd}_{y}}{\mathrm{OperationalLife}_{r,t}} \right) \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{DepreciationMethod}_{r} = 1 \wedge \mathrm{OperationalLife}_{r,t} > \mathrm{YearsUntilEnd}_{y} \wedge \mathrm{DiscountRate}_{r} = 0 \vee \mathrm{DepreciationMethod}_{r} = 2 \wedge \mathrm{OperationalLife}_{r,t} > \mathrm{YearsUntilEnd}_{y}
```

**`SV3_SalvageValueAtEndOfPeriod3`**

```math
\mathit{SalvageValue}_{r,t,y} = 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{OperationalLife}_{r,t} \le \mathrm{YearsUntilEnd}_{y}
```

**`SV4_SalvageValueDiscountedToStartYear`**

```math
\mathit{DiscountedSalvageValue}_{r,t,y} = \frac{\mathit{SalvageValue}_{r,t,y}}{\left( 1 + \mathrm{DiscountRate}_{r} \right)^{\mathrm{YearsSinceStart}_{y} + \mathrm{YearsUntilEnd}_{y}}} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`OC1_OperatingCostsVariable`**

```math
\sum_{o \in \mathcal{O}} \mathit{TotalAnnualTechnologyActivityByMode}_{r,t,o,y} \cdot \mathrm{VariableCost}_{r,t,o,y} = \mathit{AnnualVariableOperatingCost}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \sum_{o \in \mathcal{O}} \mathrm{VariableCost}_{r,t,o,y} \neq 0
```

**`OC2_OperatingCostsFixedAnnual`**

```math
\mathit{TotalCapacityAnnual}_{r,t,y} \cdot \mathrm{FixedCost}_{r,t,y} = \mathit{AnnualFixedOperatingCost}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`OC3_OperatingCostsTotalAnnual`**

```math
\mathit{AnnualFixedOperatingCost}_{r,t,y} + \mathit{AnnualVariableOperatingCost}_{r,t,y} = \mathit{OperatingCost}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`OC4_DiscountedOperatingCostsTotalAnnual`**

```math
\frac{\mathit{OperatingCost}_{r,t,y}}{\mathrm{DiscountFactorMid}_{r,y}} = \mathit{DiscountedOperatingCost}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TDC1_TotalDiscountedCostByTechnology`**

```math
\mathit{DiscountedOperatingCost}_{r,t,y} + \mathit{DiscountedCapitalInvestment}_{r,t,y} + \mathit{DiscountedTechnologyEmissionsPenalty}_{r,t,y} - \mathit{DiscountedSalvageValue}_{r,t,y} = \mathit{TotalDiscountedCostByTechnology}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TDC2_TotalDiscountedCost`**

```math
\sum_{t \in \mathcal{T}} \mathit{TotalDiscountedCostByTechnology}_{r,t,y} + \sum_{g \in \mathcal{G}} \mathit{TotalDiscountedStorageCost}_{r,g,y} = \mathit{TotalDiscountedCost}_{r,y} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`TCC1_TotalAnnualMaxCapacityConstraint`**

```math
\mathit{TotalCapacityAnnual}_{r,t,y} \le \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \neq -1
```

**`TCC2_TotalAnnualMinCapacityConstraint`**

```math
\mathit{TotalCapacityAnnual}_{r,t,y} \ge \mathrm{TotalAnnualMinCapacity}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMinCapacity}_{r,t,y} > 0
```

**`NCC1_TotalAnnualMaxNewCapacityConstraint`**

```math
\mathit{NewCapacity}_{r,t,y} \le \mathrm{TotalAnnualMaxCapacityInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacityInvestment}_{r,t,y} \neq -1
```

**`NCC2_TotalAnnualMinNewCapacityConstraint`**

```math
\mathit{NewCapacity}_{r,t,y} \ge \mathrm{TotalAnnualMinCapacityInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMinCapacityInvestment}_{r,t,y} > 0
```

**`AAC1_TotalAnnualTechnologyActivity`**

```math
\sum_{i \in \mathcal{I}} \mathit{RateOfTotalActivity}_{r,t,i,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{TotalTechnologyAnnualActivity}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`AAC2_TotalAnnualTechnologyActivityUpperLimit`**

```math
\mathit{TotalTechnologyAnnualActivity}_{r,t,y} \le \mathrm{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y} \neq -1
```

**`AAC3_TotalAnnualTechnologyActivityLowerLimit`**

```math
\mathit{TotalTechnologyAnnualActivity}_{r,t,y} \ge \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} > 0
```

**`TAC1_TotalModelHorizonTechnologyActivity`**

```math
\sum_{y \in \mathcal{Y}} \mathit{TotalTechnologyAnnualActivity}_{r,t,y} = \mathit{TotalTechnologyModelPeriodActivity}_{r,t} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T}
```

**`TAC2_TotalModelHorizonTechnologyActivityUpperLimit`**

```math
\mathit{TotalTechnologyModelPeriodActivity}_{r,t} \le \mathrm{TotalTechnologyModelPeriodActivityUpperLimit}_{r,t} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T} \,:\, \mathrm{TotalTechnologyModelPeriodActivityUpperLimit}_{r,t} \neq -1
```

**`TAC3_TotalModelHorizenTechnologyActivityLowerLimit`**

```math
\mathit{TotalTechnologyModelPeriodActivity}_{r,t} \ge \mathrm{TotalTechnologyModelPeriodActivityLowerLimit}_{r,t} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T} \,:\, \mathrm{TotalTechnologyModelPeriodActivityLowerLimit}_{r,t} > 0
```

**`RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units`**

```math
\sum_{t \in \mathcal{T}} \mathit{TotalCapacityAnnual}_{r,t,y} \cdot \mathrm{ReserveMarginTagTechnology}_{r,t,y} \cdot \mathrm{CapacityToActivityUnit}_{r,t} = \mathit{TotalCapacityInReserveMargin}_{r,y} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y} \,:\, \mathrm{ReserveMargin}_{r,y} > 0
```

**`RM2_ReserveMargin_FuelsIncluded`**

```math
\sum_{f \in \mathcal{F}} \mathit{RateOfProduction}_{r,i,f,y} \cdot \mathrm{ReserveMarginTagFuel}_{r,f,y} = \mathit{DemandNeedingReserveMargin}_{r,i,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ y \in \mathcal{Y} \,:\, \mathrm{ReserveMargin}_{r,y} > 0
```

**`RM3_ReserveMargin_Constraint`**

```math
\mathit{DemandNeedingReserveMargin}_{r,i,y} \cdot \mathrm{ReserveMargin}_{r,y} \le \mathit{TotalCapacityInReserveMargin}_{r,y} \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ y \in \mathcal{Y} \,:\, \mathrm{ReserveMargin}_{r,y} > 0
```

**`RE1_FuelProductionByTechnologyAnnual`**

```math
\sum_{i \in \mathcal{I}} \mathit{ProductionByTechnology}_{r,i,t,f,y} = \mathit{ProductionByTechnologyAnnual}_{r,t,f,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`RE2_TechIncluded`**

```math
\sum_{f \in \mathcal{F}} \sum_{t \in \mathcal{T}} \mathit{ProductionByTechnologyAnnual}_{r,t,f,y} \cdot \mathrm{RETagTechnology}_{r,t,y} = \mathit{TotalREProductionAnnual}_{r,y} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`RE3_FuelIncluded`**

```math
\sum_{f \in \mathcal{F}} \sum_{i \in \mathcal{I}} \mathit{RateOfProduction}_{r,i,f,y} \cdot \mathrm{YearSplit}_{i,y} \cdot \mathrm{RETagFuel}_{r,f,y} = \mathit{RETotalProductionOfTargetFuelAnnual}_{r,y} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`RE4_EnergyConstraint`**

```math
\mathrm{REMinProductionTarget}_{r,y} \cdot \mathit{RETotalProductionOfTargetFuelAnnual}_{r,y} \le \mathit{TotalREProductionAnnual}_{r,y} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`RE5_FuelUseByTechnologyAnnual`**

```math
\sum_{i \in \mathcal{I}} \mathit{RateOfUseByTechnology}_{r,i,t,f,y} \cdot \mathrm{YearSplit}_{i,y} = \mathit{UseByTechnologyAnnual}_{r,t,f,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`E1_AnnualEmissionProductionByMode`**

```math
\mathrm{EmissionActivityRatio}_{r,t,m,o,y} \cdot \mathit{TotalAnnualTechnologyActivityByMode}_{r,t,o,y} = \mathit{AnnualTechnologyEmissionByMode}_{r,t,m,o,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ o \in \mathcal{O},\ y \in \mathcal{Y} \,:\, \mathrm{EmissionActivityRatio}_{r,t,m,o,y} \neq 0
```

**`E2_AnnualEmissionProduction`**

```math
\sum_{o \in \mathcal{O}} \mathit{AnnualTechnologyEmissionByMode}_{r,t,m,o,y} = \mathit{AnnualTechnologyEmission}_{r,t,m,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ y \in \mathcal{Y}
```

**`E3_EmissionsPenaltyByTechAndEmission`**

```math
\mathit{AnnualTechnologyEmission}_{r,t,m,y} \cdot \mathrm{EmissionsPenalty}_{r,m,y} = \mathit{AnnualTechnologyEmissionPenaltyByEmission}_{r,t,m,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ y \in \mathcal{Y} \,:\, \mathrm{EmissionsPenalty}_{r,m,y} \neq 0
```

**`E4_EmissionsPenaltyByTechnology`**

```math
\sum_{m \in \mathcal{M}} \mathit{AnnualTechnologyEmissionPenaltyByEmission}_{r,t,m,y} = \mathit{AnnualTechnologyEmissionsPenalty}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`E5_DiscountedEmissionsPenaltyByTechnology`**

```math
\frac{\mathit{AnnualTechnologyEmissionsPenalty}_{r,t,y}}{\mathrm{DiscountFactorMid}_{r,y}} = \mathit{DiscountedTechnologyEmissionsPenalty}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`E6_EmissionsAccounting1`**

```math
\sum_{t \in \mathcal{T}} \mathit{AnnualTechnologyEmission}_{r,t,m,y} = \mathit{AnnualEmissions}_{r,m,y} \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M},\ y \in \mathcal{Y}
```

**`E7_EmissionsAccounting2`**

```math
\sum_{y \in \mathcal{Y}} \mathit{AnnualEmissions}_{r,m,y} = \mathit{ModelPeriodEmissions}_{r,m} - \mathrm{ModelPeriodExogenousEmission}_{r,m} \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M}
```

**`E8_AnnualEmissionsLimit`**

```math
\mathit{AnnualEmissions}_{r,m,y} + \mathrm{AnnualExogenousEmission}_{r,m,y} \le \mathrm{AnnualEmissionLimit}_{r,m,y} \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M},\ y \in \mathcal{Y} \,:\, \mathrm{AnnualEmissionLimit}_{r,m,y} \neq -1
```

**`E9_ModelPeriodEmissionsLimit`**

```math
\mathit{ModelPeriodEmissions}_{r,m} \le \mathrm{ModelPeriodEmissionLimit}_{r,m} \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M} \,:\, \mathrm{ModelPeriodEmissionLimit}_{r,m} \neq -1
```

#### Definitions

**`DiscountFactor`**

```math
\mathrm{DiscountFactor}_{r,y} = \left( 1 + \mathrm{DiscountRate}_{r} \right)^{\mathrm{YearsSinceStart}_{y}} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`DiscountFactorMid`**

```math
\mathrm{DiscountFactorMid}_{r,y} = \left( 1 + \mathrm{DiscountRate}_{r} \right)^{\mathrm{YearsSinceStart}_{y} + 0.5} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`CapitalRecoveryFactor`**

```math
\mathrm{CapitalRecoveryFactor}_{r,t} = \frac{1 - \left( 1 + \mathrm{DiscountRateIdv}_{r,t} \right)^{-1}}{1 - \left( 1 + \mathrm{DiscountRateIdv}_{r,t} \right)^{-\mathrm{OperationalLife}_{r,t}}} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T}
```

**`PvAnnuity`**

```math
\mathrm{PvAnnuity}_{r,t} = \frac{\left( 1 - \left( 1 + \mathrm{DiscountRate}_{r} \right)^{-\mathrm{OperationalLife}_{r,t}} \right) \cdot \left( 1 + \mathrm{DiscountRate}_{r} \right)}{\mathrm{DiscountRate}_{r}} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T}
```

**`DiscountFactorStorage`**

```math
\mathrm{DiscountFactorStorage}_{r,g,y} = \left( 1 + \mathrm{DiscountRateStorage}_{r,g} \right)^{\mathrm{YearsSinceStart}_{y}} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`DiscountFactorMidStorage`**

```math
\mathrm{DiscountFactorMidStorage}_{r,g,y} = \left( 1 + \mathrm{DiscountRateStorage}_{r,g} \right)^{\mathrm{YearsSinceStart}_{y} + 0.5} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageLevelYearStartCarried`**

```math
\mathit{StorageLevelYearStartCarried}_{r,g,y} = \begin{cases} \mathrm{StorageLevelStart}_{r,g} & \text{if } \mathrm{pos}(y) = 0 \\ \mathit{StorageLevelYearStart}_{r,g,y - 1} + \sum_{a \in \mathcal{A}} \sum_{d \in \mathcal{D}} \sum_{s \in \mathcal{S}} \mathit{NetChargeWithinYear}_{r,g,s,d,a,y - 1} & \text{otherwise} \end{cases} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageLevelYearFinishCarried`**

```math
\mathit{StorageLevelYearFinishCarried}_{r,g,y} = \begin{cases} \mathit{StorageLevelYearStart}_{r,g,y} + \sum_{a \in \mathcal{A}} \sum_{d \in \mathcal{D}} \sum_{s \in \mathcal{S}} \mathit{NetChargeWithinYear}_{r,g,s,d,a,y} & \text{if } \mathrm{pos}(y) = \lvert \mathcal{Y} \rvert - 1 \\ \mathit{StorageLevelYearStart}_{r,g,y + 1} & \text{otherwise} \end{cases} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageLevelSeasonStartCarried`**

```math
\mathit{StorageLevelSeasonStartCarried}_{r,g,s,y} = \begin{cases} \mathit{StorageLevelYearStart}_{r,g,y} & \text{if } \mathrm{pos}(s) = 0 \\ \mathit{StorageLevelSeasonStart}_{r,g,s - 1,y} + \sum_{a \in \mathcal{A}} \sum_{d \in \mathcal{D}} \mathit{NetChargeWithinYear}_{r,g,s - 1,d,a,y} & \text{otherwise} \end{cases} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ y \in \mathcal{Y}
```

**`StorageLevelDayTypeStartCarried`**

```math
\mathit{StorageLevelDayTypeStartCarried}_{r,g,s,d,y} = \begin{cases} \mathit{StorageLevelSeasonStart}_{r,g,s,y} & \text{if } \mathrm{pos}(d) = 0 \\ \mathit{StorageLevelDayTypeStart}_{r,g,s,d - 1,y} + \sum_{a \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d - 1,a,y} \cdot \mathrm{DaysInDayType}_{s,d - 1,y} & \text{otherwise} \end{cases} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

**`StorageLevelDayTypeFinishCarried`**

```math
\mathit{StorageLevelDayTypeFinishCarried}_{r,g,s,d,y} = \begin{cases} \mathit{StorageLevelYearFinish}_{r,g,y} & \text{if } \mathrm{pos}(s) = \lvert \mathcal{S} \rvert - 1 \wedge \mathrm{pos}(d) = \lvert \mathcal{D} \rvert - 1 \\ \mathit{StorageLevelSeasonStart}_{r,g,s + 1,y} & \text{if } \mathrm{pos}(s) \neq \lvert \mathcal{S} \rvert - 1 \wedge \mathrm{pos}(d) = \lvert \mathcal{D} \rvert - 1 \\ \mathit{StorageLevelDayTypeFinish}_{r,g,s,d + 1,y} - \left( \sum_{a \in \mathcal{A}} \mathit{NetChargeWithinDay}_{r,g,s,d + 1,a,y} \cdot \mathrm{DaysInDayType}_{s,d + 1,y} \right) & \text{otherwise} \end{cases} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

#### Variable domains

**`RateOfDemand`**

```math
\mathit{RateOfDemand}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Demand`**

```math
\mathit{Demand}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`RateOfStorageCharge`**

```math
\mathit{RateOfStorageCharge}_{r,g,s,d,a,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`RateOfStorageDischarge`**

```math
\mathit{RateOfStorageDischarge}_{r,g,s,d,a,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`NetChargeWithinYear`**

```math
\mathit{NetChargeWithinYear}_{r,g,s,d,a,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`NetChargeWithinDay`**

```math
\mathit{NetChargeWithinDay}_{r,g,s,d,a,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ a \in \mathcal{A},\ y \in \mathcal{Y}
```

**`StorageLevelYearStart`**

```math
\mathit{StorageLevelYearStart}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageLevelYearFinish`**

```math
\mathit{StorageLevelYearFinish}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageLevelSeasonStart`**

```math
\mathit{StorageLevelSeasonStart}_{r,g,s,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ y \in \mathcal{Y}
```

**`StorageLevelDayTypeStart`**

```math
\mathit{StorageLevelDayTypeStart}_{r,g,s,d,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

**`StorageLevelDayTypeFinish`**

```math
\mathit{StorageLevelDayTypeFinish}_{r,g,s,d,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ s \in \mathcal{S},\ d \in \mathcal{D},\ y \in \mathcal{Y}
```

**`StorageLowerLimit`**

```math
\mathit{StorageLowerLimit}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`StorageUpperLimit`**

```math
\mathit{StorageUpperLimit}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`AccumulatedNewStorageCapacity`**

```math
\mathit{AccumulatedNewStorageCapacity}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`NewStorageCapacity`**

```math
\mathit{NewStorageCapacity}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`CapitalInvestmentStorage`**

```math
\mathit{CapitalInvestmentStorage}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`DiscountedCapitalInvestmentStorage`**

```math
\mathit{DiscountedCapitalInvestmentStorage}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`SalvageValueStorage`**

```math
\mathit{SalvageValueStorage}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`DiscountedSalvageValueStorage`**

```math
\mathit{DiscountedSalvageValueStorage}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`TotalDiscountedStorageCost`**

```math
\mathit{TotalDiscountedStorageCost}_{r,g,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G},\ y \in \mathcal{Y}
```

**`NumberOfNewTechnologyUnits`**

```math
\mathit{NumberOfNewTechnologyUnits}_{r,t,y} \ge 0, \mathit{NumberOfNewTechnologyUnits}_{r,t,y} \in \mathbb{Z} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{CapacityOfOneTechnologyUnit}_{r,t,y} \neq 0
```

**`NewCapacity`**

```math
\mathit{NewCapacity}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`AccumulatedNewCapacity`**

```math
\mathit{AccumulatedNewCapacity}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TotalCapacityAnnual`**

```math
\mathit{TotalCapacityAnnual}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`RateOfActivity`**

```math
\mathit{RateOfActivity}_{r,i,t,o,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ o \in \mathcal{O},\ y \in \mathcal{Y}
```

**`RateOfTotalActivity`**

```math
\mathit{RateOfTotalActivity}_{r,t,i,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ i \in \mathcal{I},\ y \in \mathcal{Y}
```

**`TotalTechnologyAnnualActivity`**

```math
\mathit{TotalTechnologyAnnualActivity}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TotalAnnualTechnologyActivityByMode`**

```math
\mathit{TotalAnnualTechnologyActivityByMode}_{r,t,o,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ o \in \mathcal{O},\ y \in \mathcal{Y}
```

**`TotalTechnologyModelPeriodActivity`**

```math
\mathit{TotalTechnologyModelPeriodActivity}_{r,t} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T}
```

**`RateOfProductionByTechnologyByMode`**

```math
\mathit{RateOfProductionByTechnologyByMode}_{r,i,t,o,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ o \in \mathcal{O},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \mathrm{OutputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`RateOfProductionByTechnology`**

```math
\mathit{RateOfProductionByTechnology}_{r,i,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`ProductionByTechnology`**

```math
\mathit{ProductionByTechnology}_{r,i,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`ProductionByTechnologyAnnual`**

```math
\mathit{ProductionByTechnologyAnnual}_{r,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`RateOfProduction`**

```math
\mathit{RateOfProduction}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Production`**

```math
\mathit{Production}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`RateOfUseByTechnologyByMode`**

```math
\mathit{RateOfUseByTechnologyByMode}_{r,i,t,o,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ o \in \mathcal{O},\ f \in \mathcal{F},\ y \in \mathcal{Y} \,:\, \mathrm{InputActivityRatio}_{r,t,f,o,y} \neq 0
```

**`RateOfUseByTechnology`**

```math
\mathit{RateOfUseByTechnology}_{r,i,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`UseByTechnologyAnnual`**

```math
\mathit{UseByTechnologyAnnual}_{r,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`RateOfUse`**

```math
\mathit{RateOfUse}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`UseByTechnology`**

```math
\mathit{UseByTechnology}_{r,i,t,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ t \in \mathcal{T},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Use`**

```math
\mathit{Use}_{r,i,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`Trade`**

```math
\mathit{Trade}_{r,e,i,f,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ e \in \mathcal{E},\ i \in \mathcal{I},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`TradeAnnual`**

```math
\mathit{TradeAnnual}_{r,e,f,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ e \in \mathcal{E},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`ProductionAnnual`**

```math
\mathit{ProductionAnnual}_{r,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`UseAnnual`**

```math
\mathit{UseAnnual}_{r,f,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`CapitalInvestment`**

```math
\mathit{CapitalInvestment}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`DiscountedCapitalInvestment`**

```math
\mathit{DiscountedCapitalInvestment}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`SalvageValue`**

```math
\mathit{SalvageValue}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`DiscountedSalvageValue`**

```math
\mathit{DiscountedSalvageValue}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`OperatingCost`**

```math
\mathit{OperatingCost}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`DiscountedOperatingCost`**

```math
\mathit{DiscountedOperatingCost}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`AnnualVariableOperatingCost`**

```math
\mathit{AnnualVariableOperatingCost}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`AnnualFixedOperatingCost`**

```math
\mathit{AnnualFixedOperatingCost}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TotalDiscountedCostByTechnology`**

```math
\mathit{TotalDiscountedCostByTechnology}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`TotalDiscountedCost`**

```math
\mathit{TotalDiscountedCost}_{r,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`ModelPeriodCostByRegion`**

```math
\mathit{ModelPeriodCostByRegion}_{r} \ge 0 \qquad \forall\, r \in \mathcal{R}
```

**`TotalCapacityInReserveMargin`**

```math
\mathit{TotalCapacityInReserveMargin}_{r,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`DemandNeedingReserveMargin`**

```math
\mathit{DemandNeedingReserveMargin}_{r,i,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ i \in \mathcal{I},\ y \in \mathcal{Y}
```

**`TotalREProductionAnnual`**

```math
\mathit{TotalREProductionAnnual}_{r,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`RETotalProductionOfTargetFuelAnnual`**

```math
\mathit{RETotalProductionOfTargetFuelAnnual}_{r,y} \in \mathbb{R} \qquad \forall\, r \in \mathcal{R},\ y \in \mathcal{Y}
```

**`AnnualTechnologyEmissionByMode`**

```math
\mathit{AnnualTechnologyEmissionByMode}_{r,t,m,o,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ o \in \mathcal{O},\ y \in \mathcal{Y}
```

**`AnnualTechnologyEmission`**

```math
\mathit{AnnualTechnologyEmission}_{r,t,m,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ y \in \mathcal{Y}
```

**`AnnualTechnologyEmissionPenaltyByEmission`**

```math
\mathit{AnnualTechnologyEmissionPenaltyByEmission}_{r,t,m,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ m \in \mathcal{M},\ y \in \mathcal{Y}
```

**`AnnualTechnologyEmissionsPenalty`**

```math
\mathit{AnnualTechnologyEmissionsPenalty}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`DiscountedTechnologyEmissionsPenalty`**

```math
\mathit{DiscountedTechnologyEmissionsPenalty}_{r,t,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`AnnualEmissions`**

```math
\mathit{AnnualEmissions}_{r,m,y} \ge 0 \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M},\ y \in \mathcal{Y}
```

**`ModelPeriodEmissions`**

```math
\mathit{ModelPeriodEmissions}_{r,m} \ge 0 \qquad \forall\, r \in \mathcal{R},\ m \in \mathcal{M}
```

#### Assumptions

**`capacity_investment_bounds_do_not_cross`**

```math
\mathrm{TotalAnnualMaxCapacityInvestment}_{r,t,y} \ge \mathrm{TotalAnnualMinCapacityInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacityInvestment}_{r,t,y} \neq -1 \wedge \mathrm{TotalAnnualMinCapacityInvestment}_{r,t,y} \neq 0
```

**`annual_activity_limits_do_not_cross`**

```math
\mathrm{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y} \ge \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y} \neq -1 \wedge \mathrm{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y} \neq 0 \wedge \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \neq 0
```

**`residual_capacity_within_max_capacity`**

```math
\mathrm{TotalAnnualMaxCapacity}_{r,t,y} \ge \mathrm{ResidualCapacity}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \neq -1 \wedge \mathrm{ResidualCapacity}_{r,t,y} \neq 0
```

**`residual_and_min_investment_within_max_capacity`**

```math
\mathrm{TotalAnnualMaxCapacity}_{r,t,y} \ge \mathrm{ResidualCapacity}_{r,t,y} + \mathrm{TotalAnnualMinCapacityInvestment}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \neq -1 \wedge \mathrm{ResidualCapacity}_{r,t,y} \neq 0
```

**`max_capacity_can_meet_min_activity`**

```math
\left( \sum_{i \in \mathcal{I}} \mathrm{CapacityFactor}_{r,t,i,y} \cdot \mathrm{YearSplit}_{i,y} \right) \cdot \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \cdot \mathrm{AvailabilityFactor}_{r,t,y} \cdot \mathrm{CapacityToActivityUnit}_{r,t} \ge \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y} \,:\, \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \neq 0 \wedge \mathrm{TotalAnnualMaxCapacity}_{r,t,y} \neq -1 \wedge \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \neq 0 \wedge \mathrm{AvailabilityFactor}_{r,t,y} \neq 0 \wedge \mathrm{CapacityToActivityUnit}_{r,t} \neq 0
```

**`year_split_sums_to_one`**

```math
\sum_{i \in \mathcal{I}} \mathrm{YearSplit}_{i,y} \ge 0.9999 \wedge \sum_{i \in \mathcal{I}} \mathrm{YearSplit}_{i,y} \le 1.0001 \qquad \forall\, y \in \mathcal{Y}
```

**`model_period_activity_limit_covers_annual_limits`**

```math
\mathrm{TotalTechnologyModelPeriodActivityLowerLimit}_{r,t} \ge \sum_{y \in \mathcal{Y}} \mathrm{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y} \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T} \,:\, \mathrm{TotalTechnologyModelPeriodActivityLowerLimit}_{r,t} \neq 0
```

**`years_since_start_counts_from_the_first_year`**

```math
\mathrm{YearsSinceStart}_{y} = 0 \qquad \forall\, y \in \mathcal{Y} \,:\, \mathrm{pos}(y) = 0
```

**`years_until_end_counts_to_the_last_year`**

```math
\mathrm{YearsUntilEnd}_{y} = 1 \qquad \forall\, y \in \mathcal{Y} \,:\, \mathrm{pos}(y) = \lvert \mathcal{Y} \rvert - 1
```

**`operational_life_is_not_negative`**

```math
\mathrm{OperationalLife}_{r,t} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T}
```

**`operational_life_storage_is_not_negative`**

```math
\mathrm{OperationalLifeStorage}_{r,g} \ge 0 \qquad \forall\, r \in \mathcal{R},\ g \in \mathcal{G}
```

**`storage_shares_are_non_negative`**

```math
\mathrm{TechnologyToStorage}_{r,t,g,o} \ge 0 \wedge \mathrm{TechnologyFromStorage}_{r,t,g,o} \ge 0 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ o \in \mathcal{O},\ g \in \mathcal{G}
```

**`conversion_ls_is_binary`**

```math
\mathrm{Conversionls}_{i,s} = 0 \vee \mathrm{Conversionls}_{i,s} = 1 \qquad \forall\, i \in \mathcal{I},\ s \in \mathcal{S}
```

**`conversion_ld_is_binary`**

```math
\mathrm{Conversionld}_{i,d} = 0 \vee \mathrm{Conversionld}_{i,d} = 1 \qquad \forall\, i \in \mathcal{I},\ d \in \mathcal{D}
```

**`conversion_lh_is_binary`**

```math
\mathrm{Conversionlh}_{i,a} = 0 \vee \mathrm{Conversionlh}_{i,a} = 1 \qquad \forall\, i \in \mathcal{I},\ a \in \mathcal{A}
```

**`trade_route_is_binary`**

```math
\mathrm{TradeRoute}_{r,e,f,y} = 0 \vee \mathrm{TradeRoute}_{r,e,f,y} = 1 \qquad \forall\, r \in \mathcal{R},\ e \in \mathcal{E},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`reserve_margin_tag_technology_is_a_share`**

```math
\mathrm{ReserveMarginTagTechnology}_{r,t,y} \ge 0 \wedge \mathrm{ReserveMarginTagTechnology}_{r,t,y} \le 1 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`reserve_margin_tag_fuel_is_binary`**

```math
\mathrm{ReserveMarginTagFuel}_{r,f,y} = 0 \vee \mathrm{ReserveMarginTagFuel}_{r,f,y} = 1 \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

**`re_tag_technology_is_binary`**

```math
\mathrm{RETagTechnology}_{r,t,y} = 0 \vee \mathrm{RETagTechnology}_{r,t,y} = 1 \qquad \forall\, r \in \mathcal{R},\ t \in \mathcal{T},\ y \in \mathcal{Y}
```

**`re_tag_fuel_is_binary`**

```math
\mathrm{RETagFuel}_{r,f,y} = 0 \vee \mathrm{RETagFuel}_{r,f,y} = 1 \qquad \forall\, r \in \mathcal{R},\ f \in \mathcal{F},\ y \in \mathcal{Y}
```

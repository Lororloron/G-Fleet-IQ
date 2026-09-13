from decimal import Decimal


# ==========================================================
# PROFIT ENGINE
# ==========================================================

def calculate_load_profit(load):

    revenue = Decimal(load.rate or 0)

    miles = Decimal(
        load.miles or load.distance or 0
    )

    # ======================================================
    # FUEL
    # ======================================================

    # Use the assigned driver's fuel efficiency.
    # Fall back to 7.0 MPG when no driver is assigned.
    driver = getattr(load, "driver", None)

    driver_mpg = getattr(
        driver,
        "fuel_efficiency",
        None,
    )

    if driver_mpg:
        mpg = Decimal(str(driver_mpg))
    else:
        mpg = Decimal("7.0")

    # Default diesel price
    fuel_price = Decimal("3.75")

    # Calculate fuel automatically
    if miles > 0 and mpg > 0:
        gallons = miles / mpg
        fuel_cost = gallons * fuel_price
    else:
        gallons = Decimal("0")
        fuel_cost = Decimal("0")

    # ======================================================
    # OTHER EXPENSES
    # ======================================================

    driver_pay = Decimal(
        load.driver_pay or 0
    )

    tolls = Decimal(
        load.tolls or 0
    )

    maintenance_cost = Decimal(
        load.maintenance_cost or 0
    )

    insurance_cost = Decimal(
        load.insurance_cost or 0
    )

    total_expenses = (
        fuel_cost
        + driver_pay
        + tolls
        + maintenance_cost
        + insurance_cost
    )

    # ======================================================
    # PROFIT
    # ======================================================

    profit = revenue - total_expenses

    if miles > 0:
        profit_per_mile = profit / miles
    else:
        profit_per_mile = Decimal("0")

    return {
        "revenue": revenue,
        "miles": miles,
        "mpg": mpg,
        "gallons": gallons,
        "fuel_price": fuel_price,
        "fuel_cost": fuel_cost,
        "driver_pay": driver_pay,
        "tolls": tolls,
        "maintenance_cost": maintenance_cost,
        "insurance_cost": insurance_cost,
        "total_expenses": total_expenses,
        "profit": profit,
        "profit_per_mile": profit_per_mile,
    }


# ==========================================================
# SAVE PROFIT
# ==========================================================

def save_load_profit(load):

    result = calculate_load_profit(load)

    load.fuel_cost = result["fuel_cost"]
    load.profit = result["profit"]
    load.profit_per_mile = result["profit_per_mile"]

    load.save(
        update_fields=[
            "fuel_cost",
            "profit",
            "profit_per_mile",
        ]
    )

    return result
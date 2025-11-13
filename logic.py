CAP = 2000.0
MONTHS_IN_YEAR = 12


SPENDING_WEIGHTS = [
    0.15,  # Ja
    0.12,  # Fe
    0.11,  # Ma
    0.10,  # Ap
    0.10,  # Ma
    0.08,  # Jun
    0.08,  # Jul
    0.07,  # Au
    0.07,  # Se
    0.06,  # Oc
    0.04,  # No
    0.02,  # De
]


def _build_spending(annual_oop_estimate: float, cap: float | None) -> list[float]:
    """
    Build the month-by-month spending pattern.

    - annual_oop_estimate: user estimate of annual out of pocket
    - cap: if not None, cap total spending at this value (e.g. CAP).
      If None, do not cap.

    Uses a fixed front-loaded pattern and adjusts for any tiny rounding error.
    """
    total = max(annual_oop_estimate, 0.0)

  
    if cap is not None:
        total = min(total, cap)

    if total == 0:
        return [0.0] * MONTHS_IN_YEAR

    baseline = [w * total for w in SPENDING_WEIGHTS]

   
    diff = total - sum(baseline)
    baseline[-1] += diff

    return baseline


def compute_monthly_no_cap(annual_oop_estimate: float) -> list[float]:
    """
    Scenario 1: No cap at all.
    Apply the front-loaded pattern to the full annual estimate.
    """
    return _build_spending(annual_oop_estimate, cap=None)


def compute_monthly_without_smoothing(annual_oop_estimate: float) -> list[float]:
    """
    Scenario 2: Cap at 2000, no monthly payment plan.
    Apply the front-loaded pattern, but cap total at CAP.
    """
    return _build_spending(annual_oop_estimate, cap=CAP)


def compute_monthly_with_smoothing(annual_oop_estimate: float, start_month: int) -> list[float]:
    """
    Scenario 3: Cap at 2000, with monthly payment (smoothing) plan.

    Educational model:

    - Cap annual out of pocket at CAP.
    - Use the same front-loaded pattern as the 'no smoothing' case.
    - The beneficiary enrolls in smoothing at `start_month` (1–12).

    Before start_month:
        They pay the natural front-loaded monthly amounts.

    From start_month to December:
        We take the remaining balance (under the cap) and spread it evenly
        over the remaining months.

    Returns a list of 12 floats: what the beneficiary pays each month.
    """

    if start_month < 1:
        start_month = 1
    elif start_month > 12:
        start_month = 12


    baseline_cap = compute_monthly_without_smoothing(annual_oop_estimate)
    total_cap = sum(baseline_cap)

    if total_cap == 0:
        return [0.0] * MONTHS_IN_YEAR

    payments = [0.0] * MONTHS_IN_YEAR


    for month in range(1, start_month):
        payments[month - 1] = baseline_cap[month - 1]

  
    paid_so_far = sum(baseline_cap[: start_month - 1])
    remaining_balance = max(total_cap - paid_so_far, 0.0)

    remaining_months = MONTHS_IN_YEAR - (start_month - 1)

    if remaining_months <= 0 or remaining_balance == 0:
 
        return payments

    smoothed_monthly = remaining_balance / remaining_months

    for month in range(start_month, MONTHS_IN_YEAR + 1):
        payments[month - 1] = smoothed_monthly

   
    total_paid = sum(payments)
    if total_paid > total_cap:
        diff = total_paid - total_cap
        payments[-1] -= diff

    return payments

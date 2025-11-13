from logic import compute_monthly_without_smoothing, compute_monthly_with_smoothing
import matplotlib.pyplot as plt


def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_int_month(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 12:
                return value
            print("Please enter a month number between 1 and 12.")
        except ValueError:
            print("Please enter a valid integer between 1 and 12.")


def main():
    print("Medicare Part D 2025 Out-of-Pocket Cap Calculator")
    print("-------------------------------------------------")
    print("This tool uses a simplified model to illustrate the $2,000 annual cap")
    print("and the optional monthly payment (smoothing) plan.\n")

    annual_oop_estimate = get_float(
        "Estimated annual out-of-pocket spending on Part D drugs (before the cap): $"
    )
    start_month = get_int_month(
        "Month you enroll in the monthly payment option (1 = January, 12 = December): "
    )

    # Compute paths
    no_smooth = compute_monthly_without_smoothing(annual_oop_estimate)
    smooth = compute_monthly_with_smoothing(annual_oop_estimate, start_month)

    months = list(range(1, 13))

    total_no_smooth = sum(no_smooth)
    total_smooth = sum(smooth)

    print("\nRESULTS")
    print("-------")
    print(f"Total paid WITHOUT smoothing (capped at $2,000): ${total_no_smooth:,.2f}")
    print(f"Total paid WITH smoothing (capped at $2,000):    ${total_smooth:,.2f}")
    print(
        "\nNote: The monthly payment plan does not reduce your total cost; "
        "it spreads payments over remaining months."
    )

    # Plot the two monthly paths
    plt.figure()
    plt.plot(months, no_smooth, marker="o", label="Without smoothing")
    plt.plot(months, smooth, marker="o", linestyle="--", label="With smoothing")

    plt.title(
        f"Monthly payments in 2025\nAnnual estimate = ${annual_oop_estimate:,.0f}, "
        f"smoothing start month = {start_month}"
    )
    plt.xlabel("Month")
    plt.ylabel("Monthly payment ($)")
    plt.xticks(months)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

from logic import compute_monthly_without_smoothing, compute_monthly_with_smoothing
import matplotlib.pyplot as plt


def plot_scenario(annual_oop_estimate: float, start_month: int):

    no_smooth = compute_monthly_without_smoothing(annual_oop_estimate)
    smooth = compute_monthly_with_smoothing(annual_oop_estimate, start_month)

    months = list(range(1, 13))


    plt.figure()
    plt.plot(months, no_smooth, marker="o", label="Without smoothing")
    plt.plot(months, smooth, marker="o", linestyle="--", label="With smoothing")

    plt.title(f"Monthly payments, annual OOP estimate = ${annual_oop_estimate:.0f}, start_month = {start_month}")
    plt.xlabel("Month")
    plt.xticks(months)
    plt.ylabel("Monthly payment ($)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_scenario(3000, 1)

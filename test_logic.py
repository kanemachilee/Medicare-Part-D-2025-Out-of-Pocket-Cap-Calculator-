from logic import compute_monthly_without_smoothing, compute_monthly_with_smoothing

def pretty_print(label, values):
    print(label)
    for i, v in enumerate(values, start=1):
        print(f"Month {i:2d}: {v:8.2f}")
    print(f"Total: {sum(values):.2f}")
    print("-" * 30)


def main():
    # Scenario 1: High spend, $3000 estimated OOP, smoothing off
    no_smooth = compute_monthly_without_smoothing(3000)
    pretty_print("No smoothing, annual estimate $3000", no_smooth)

    # Scenario 2: High spend, $3000, smoothing on from January
    smooth_jan = compute_monthly_with_smoothing(3000, 1)
    pretty_print("Smoothing ON from January, annual estimate $3000", smooth_jan)

    # Scenario 3: High spend, $3000, smoothing on from July
    smooth_july = compute_monthly_with_smoothing(3000, 7)
    pretty_print("Smoothing ON from July, annual estimate $3000", smooth_july)

    # Scenario 4: Lower spend, $1500, smoothing on from January
    smooth_low = compute_monthly_with_smoothing(1500, 1)
    pretty_print("Smoothing ON from January, annual estimate $1500", smooth_low)


if __name__ == "__main__":
    main()

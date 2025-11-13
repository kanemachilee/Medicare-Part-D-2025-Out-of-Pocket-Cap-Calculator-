import tkinter as tk
from tkinter import ttk, messagebox

from logic import (
    compute_monthly_no_cap,
    compute_monthly_without_smoothing,
    compute_monthly_with_smoothing,
)

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PERSONAS = {
    "Custom": None,
    "High cost oncology patient": {
        "annual_oop": 5000.0,
        "start_month": 2,
        "description": "Very high cost drugs, likely to hit cap early in the year."
    },
    "Insulin dependent diabetic": {
        "annual_oop": 2500.0,
        "start_month": 1,
        "description": "Steady monthly use of insulin and other meds."
    },
    "Chronic condition on mixed meds": {
        "annual_oop": 1800.0,
        "start_month": 1,
        "description": "Multiple chronic medications, moderate annual costs."
    },
    "Occasional user": {
        "annual_oop": 600.0,
        "start_month": 1,
        "description": "Only occasional prescriptions through the year."
    },
}


def draw_chart(canvas, months, series_dict):
    """
    Draw a simple line chart on the given Tkinter canvas.

    series_dict: {label: [values]}
    """
    canvas.delete("all")

    width = int(canvas["width"])
    height = int(canvas["height"])
    margin = 50

    plot_left = margin
    plot_right = width - margin
    plot_top = margin
    plot_bottom = height - margin

    # Compute overall max value
    max_val = 0.0
    for values in series_dict.values():
        if values:
            max_val = max(max_val, max(values))

    if max_val <= 0:
        max_val = 1.0  # avoid division by zero

    # Draw axes
    canvas.create_line(plot_left, plot_bottom, plot_right, plot_bottom)  # X axis
    canvas.create_line(plot_left, plot_bottom, plot_left, plot_top)      # Y axis

    # Y axis labels (0, 50%, 100% of max)
    for i, frac in enumerate([0.0, 0.5, 1.0]):
        y_val = frac * max_val
        y = plot_bottom - frac * (plot_bottom - plot_top)
        canvas.create_line(plot_left - 5, y, plot_left, y)
        canvas.create_text(plot_left - 10, y, text=f"${y_val:,.0f}", anchor="e", fill="gray")

    # X axis labels (months)
    num_points = len(months)
    if num_points < 2:
        return

    def x_coord(i):
        return plot_left + (i / (num_points - 1)) * (plot_right - plot_left)

    # Draw month labels
    for i, m in enumerate(months):
        x = x_coord(i)
        canvas.create_line(x, plot_bottom, x, plot_bottom + 5)
        canvas.create_text(x, plot_bottom + 15, text=MONTH_NAMES[m - 1], anchor="n")

    # Colors for series
    colors = ["#d62728", "#1f77b4", "#2ca02c"]  # red, blue, green
    labels = list(series_dict.keys())

    for idx, label in enumerate(labels):
        values = series_dict[label]
        color = colors[idx % len(colors)]
        prev_x = None
        prev_y = None
        for i, v in enumerate(values):
            x = x_coord(i)
            y = plot_bottom - (v / max_val) * (plot_bottom - plot_top)
            # Draw point
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)
            # Draw line from previous point
            if prev_x is not None:
                canvas.create_line(prev_x, prev_y, x, y, fill=color, width=2)
            prev_x, prev_y = x, y

    # Legend
    legend_x = plot_right - 120
    legend_y = plot_top + 10
    for idx, label in enumerate(labels):
        color = colors[idx % len(colors)]
        canvas.create_rectangle(legend_x, legend_y + idx * 20,
                                legend_x + 10, legend_y + idx * 20 + 10,
                                fill=color, outline=color)
        canvas.create_text(legend_x + 15, legend_y + idx * 20 + 5,
                           text=label, anchor="w")


def run_scenario(annual_oop_estimate: float, start_month: int, persona_name: str | None):
    """
    Compute the three scenarios and return:
    - months list
    - dict of label -> values
    - explanation string
    """
    if start_month < 1:
        start_month = 1
    elif start_month > 12:
        start_month = 12

    months = list(range(1, 13))

    # Three scenarios
    no_cap = compute_monthly_no_cap(annual_oop_estimate)
    cap_no_smooth = compute_monthly_without_smoothing(annual_oop_estimate)
    cap_smooth = compute_monthly_with_smoothing(annual_oop_estimate, start_month)

    total_no_cap = sum(no_cap)
    total_cap = sum(cap_no_smooth)
    total_cap_smooth = sum(cap_smooth)

    # Key monthly peaks
    max_no_cap = max(no_cap) if no_cap else 0.0
    max_cap_no_smooth = max(cap_no_smooth) if cap_no_smooth else 0.0
    max_cap_smooth = max(cap_smooth) if cap_smooth else 0.0

    idx_no_cap = no_cap.index(max_no_cap) if max_no_cap > 0 else 0
    idx_cap_no_smooth = cap_no_smooth.index(max_cap_no_smooth) if max_cap_no_smooth > 0 else 0
    idx_cap_smooth = cap_smooth.index(max_cap_smooth) if max_cap_smooth > 0 else 0

    month_no_cap = MONTH_NAMES[idx_no_cap]
    month_cap_no_smooth = MONTH_NAMES[idx_cap_no_smooth]
    month_cap_smooth = MONTH_NAMES[idx_cap_smooth]

    avoided = max(total_no_cap - total_cap, 0.0)

    if persona_name and persona_name in PERSONAS and PERSONAS[persona_name]:
        persona_label = persona_name
    else:
        persona_label = "This example"

    explanation = (
        f"{persona_label} with an annual out of pocket estimate of "
        f"${annual_oop_estimate:,.0f}:\n\n"
        f"- Without any cap, total yearly out of pocket would be about "
        f"${total_no_cap:,.0f}.\n"
        f"- Under the 2025 $2,000 cap, yearly out of pocket is limited to "
        f"${total_cap:,.0f}, avoiding about ${avoided:,.0f} in spending.\n"
        f"- The highest monthly payment without a cap is about "
        f"${max_no_cap:,.0f} in {month_no_cap}.\n"
        f"- With the cap but no monthly payment plan, the highest monthly "
        f"payment is about ${max_cap_no_smooth:,.0f} in {month_cap_no_smooth}.\n"
        f"- After enrolling in the monthly payment plan in month {start_month}, "
        f"the highest monthly payment falls to about "
        f"${max_cap_smooth:,.0f} in {month_cap_smooth}.\n\n"
        f"The total amount owed under the cap is the same with or without "
        f"the monthly payment plan. The plan mainly changes the timing and "
        f"reduces the worst single month bill."
    )

    series_dict = {
        "No cap": no_cap,
        "Cap only": cap_no_smooth,
        "Cap + smoothing": cap_smooth,
    }

    return months, series_dict, explanation


def main():
    root = tk.Tk()
    root.title("Medicare Part D 2025 Out of Pocket Cap Explorer")

    # Persona selection
    tk.Label(root, text="Persona:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    persona_var = tk.StringVar(value="Custom")
    persona_combo = ttk.Combobox(
        root,
        textvariable=persona_var,
        values=list(PERSONAS.keys()),
        state="readonly",
        width=35,
    )
    persona_combo.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")

    # Annual OOP
    tk.Label(root, text="Estimated annual out of pocket ($):").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    annual_entry = tk.Entry(root, width=15)
    annual_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Start month
    tk.Label(root, text="Start month for monthly payment plan (1-12):").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    start_month_entry = tk.Entry(root, width=5)
    start_month_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Persona description
    persona_desc = tk.Label(root, text="", fg="gray")
    persona_desc.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)

    # Chart canvas
    tk.Label(root, text="Monthly payment chart:").grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    chart_canvas = tk.Canvas(root, width=700, height=300, bg="white", highlightthickness=1, highlightbackground="#cccccc")
    chart_canvas.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    # Explanation box
    tk.Label(root, text="Scenario explanation:").grid(
        row=6, column=0, sticky="w", padx=5, pady=5
    )
    explanation_text = tk.Text(root, width=80, height=10, wrap="word")
    explanation_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    def apply_persona(event=None):
        name = persona_var.get()
        info = PERSONAS.get(name)
        if info is None:
            # Custom
            persona_desc.config(text="Enter your own numbers.")
            return

        annual_entry.delete(0, tk.END)
        annual_entry.insert(0, str(info["annual_oop"]))

        start_month_entry.delete(0, tk.END)
        start_month_entry.insert(0, str(info["start_month"]))

        persona_desc.config(text=info.get("description", ""))

    persona_combo.bind("<<ComboboxSelected>>", apply_persona)

    # Default hint
    persona_desc.config(text="Select a persona or stay on Custom and enter your own values.")

    def on_run():
        try:
            annual_str = annual_entry.get().strip()
            start_str = start_month_entry.get().strip()

            if not annual_str:
                raise ValueError("Please enter an annual out of pocket estimate.")

            annual_val = float(annual_str)

            if not start_str:
                raise ValueError("Please enter a start month between 1 and 12.")

            start_val = int(start_str)
            if start_val < 1 or start_val > 12:
                raise ValueError("Start month must be between 1 and 12.")

            persona_name = persona_var.get()
            months, series_dict, explanation = run_scenario(annual_val, start_val, persona_name)

            draw_chart(chart_canvas, months, series_dict)

            explanation_text.delete("1.0", tk.END)
            explanation_text.insert(tk.END, explanation)

        except ValueError as e:
            messagebox.showerror("Input error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    run_button = tk.Button(root, text="Run scenario", command=on_run)
    run_button.grid(row=8, column=0, padx=5, pady=10, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    main()

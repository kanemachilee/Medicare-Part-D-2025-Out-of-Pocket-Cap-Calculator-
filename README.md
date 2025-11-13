# Medicare Part D 2025 Out-of-Pocket Cap Explorer

<img width="714" height="751" alt="Image" src="https://github.com/user-attachments/assets/15c632a5-5e0d-4bd7-944f-c05a08fbeefc" />

project to understand how the new 2025 Medicare Part D $2,000 out-of-pocket ceiling plays out month by month. CMS has a lot of documentation but not much you can interact with so this is my attempt at a simple visual explainer.
It’s a pure Python + tkinter thing (no external libraries). So if you have Python 3.11 installed, it should basically just run.

<img width="713" height="749" alt="Image" src="https://github.com/user-attachments/assets/5170cd29-c7b2-4bb5-abad-254891916547" />

<img width="713" height="749" alt="Image" src="https://github.com/user-attachments/assets/4c70cb7d-f381-435f-882c-96b808d84dd0" />

The program has 3 scenarios for the plan:

1. no cap (basically the old rules)
2. cap only (the new $2,000 annual max)
3. cap + smoothing (the optional monthly payment plan where you spread remaining costs evenly over the rest of the year)

Made a few few preset personas (oncology, insulin user, chronic meds, occasional user) based on typical spending patterns, but you can also customize.
The “logic” file went with synthetic spending curve, front-loaded because people tend to pay more earlier in the year and applies the cap and smoothing rules on top of it. This is not meant to be exact actuarial modeling by no means, just an educational illustration.

how to run:
You need Python 3.11 or newer. clone or download run python gui_app.py 





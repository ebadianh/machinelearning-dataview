"""Validering av dataset och val av target.

Ska svara på om ett dataset går att träna på och ge begripliga felmeddelanden
när det inte gör det:

- att CSV:n går att läsa och har minst ett par rader och kolumner
- att den valda target-kolumnen finns och inte är tom
- om problemet är klassificering eller regression (``problem_type``)
- att en klassificerings-target har rimligt antal klasser och att varje klass
  förekommer tillräckligt ofta för en train/test-uppdelning
- vilka kolumner som ska uteslutas (t.ex. id-liknande kolumner)
"""

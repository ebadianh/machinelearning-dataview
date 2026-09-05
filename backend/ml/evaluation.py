"""Utvärdering och jämförelse av de tränade modellerna.

Ska beräkna mätvärden på testdatan och peka ut den bästa modellen:

- klassificering: accuracy, precision, recall, f1 och confusion matrix
- regression: r2, MAE och RMSE
- sammanställa mätvärdena per modell som en dict för ``models.metrics_json``
- markera vinnaren (``models.is_best``) utifrån ett förvalt huvudmätvärde
"""

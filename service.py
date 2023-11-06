import math

def taxComputation(income_rs: int):
    # Tax computation logic
    if income_rs <= 300000:
        return 0
    elif income_rs <= 600000:
        return (income_rs - 300000) * 0.05
    elif income_rs <= 900000:
        return (income_rs - 600000) * 0.10 + 300000 * 0.05
    elif income_rs <= 1200000:
        return (income_rs - 900000) * 0.15 + 300000 * 0.10 + 300000 * 0.05
    elif income_rs <= 1500000:
        return (income_rs - 1200000) * 0.20 + 300000 * 0.15 + 300000 * 0.10 + 300000 * 0.05
    else:
        return (income_rs - 1500000) * 0.30 + 300000 * 0.20 + 300000 * 0.15 + 300000 * 0.10 + 300000 * 0.05
    
def emiCalculator(loan_amount_rs: int, rate_pa: float, tenure_yrs: int):
    # EMI computation logic
    rate_pm = rate_pa / (12 * 100)
    tenure_months = tenure_yrs * 12
    emi = loan_amount_rs * rate_pm * math.pow(1 + rate_pm, tenure_months) / (math.pow(1 + rate_pm, tenure_months) - 1)
    total = emi * tenure_months
    return emi

def FDReturnsCalculator(investment_rs: int, rate_pa: float, tenure_yrs: int):
    # Calculation of net returns from FD
    rate_pm = rate_pa / (12 * 100)
    tenure_months = tenure_yrs * 12
    total = investment_rs * math.pow(1 + rate_pm, tenure_months)
    return (total - investment_rs)

def currencyConverter(amount: int, currency: int):
    # Currency conversion logic (from INR to other currencies)
    if currency == 1:
        return amount / 80
    elif currency == 2:
        return amount / 90
    elif currency == 3:
        return amount / 100
    elif currency == 4:
        return amount / 0.63

def financialLiteracy():
    return 404
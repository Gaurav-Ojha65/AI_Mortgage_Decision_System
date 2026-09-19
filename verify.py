import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('backend'))

from ml.utils.features import applicant_to_15_features
from ml.inference.predict import predict_single, calculate_emi as ml_emi
from risk_calc import calculate_risk
from monte_carlo import simulate

def test(name, income, loan_amount, credit_score, interest_rate, loan_term, region="North"):
    loan_data = {
        'income': income, 'loan_amount': loan_amount, 'credit_score': credit_score,
        'existing_loans': 0, 'loan_term': loan_term, 'interest_rate': interest_rate
    }
    emi = ml_emi(loan_amount, interest_rate, loan_term * 12)
    loan_data['emi'] = emi
    
    f15 = applicant_to_15_features(loan_data)
    ml_result = predict_single(f15)
    approval_prob = ml_result["approval_probability"]
    
    risk = calculate_risk(income, loan_amount, credit_score, 0, emi=emi, region=region)
    mc = simulate({'income': income, 'loan_amount': loan_amount, 'interest_rate': interest_rate, 'loan_term': loan_term, 'credit_score': credit_score}, n_simulations=500)
    mc_default = mc["default_probability"]
    
    if risk == "HIGH" or mc_default > 0.40:
        decision = "REJECT"
    elif risk == "LOW" and mc_default < 0.15:
        decision = "APPROVE" if (approval_prob is None or approval_prob > 0.6) else "CONDITIONAL"
    else:
        decision = "CONDITIONAL"
    if approval_prob >= 0.85 and decision == "CONDITIONAL":
        decision = "APPROVE"
    elif approval_prob <= 0.15 and decision == "CONDITIONAL":
        decision = "REJECT"

    foir = emi/income*100
    print(f"{name}")
    print(f"  EMI={emi:,.0f} FOIR={foir:.1f}% | ML={approval_prob:.1%} | Risk={risk} | MC={mc_default:.1%} | DECISION={decision}")
    print()

print("=" * 65)
print("  FULL SYSTEM SANITY CHECK")
print("=" * 65)
test("GOOD: 750 CIBIL, 60k salary, 20L loan, 20yr",   60000,  2000000, 750, 9.0, 20)
test("GOOD: 800 CIBIL, 100k salary, 30L loan, 15yr", 100000,  3000000, 800, 9.0, 15)
test("BORDERLINE: 680 CIBIL, 50k, 15L, 20yr",         50000,  1500000, 680, 9.0, 20)
test("REJECT: 500 CIBIL, 80k, 10L, 5yr",              80000,  1000000, 500, 9.0,  5)
test("REJECT: Extreme FOIR 750 CIBIL, 30k, 40L, 20yr",30000,  4000000, 750, 9.0, 20)
test("CONDITIONAL: 700 CIBIL, 40k, 20L, 20yr",        40000,  2000000, 700, 9.0, 20)

import json
from datetime import datetime, timedelta
from collections import defaultdict

print("Feature Engineering Pipeline")
print("=" * 60)

# ── Raw data (simulating your Snowflake tables) ───────────────
raw_customers = [
    {"id": 1, "first_name": "Michael", "last_name": "P",
     "signup_date": "2023-01-15"},
    {"id": 2, "first_name": "Shawn",   "last_name": "M",
     "signup_date": "2023-03-22"},
    {"id": 3, "first_name": "Katharine","last_name": "R",
     "signup_date": "2023-06-10"},
]

raw_orders = [
    {"id": 1, "user_id": 1, "order_date": "2024-01-01",
     "status": "completed", "amount": 99.99},
    {"id": 2, "user_id": 2, "order_date": "2024-01-02",
     "status": "returned",  "amount": 49.99},
    {"id": 3, "user_id": 1, "order_date": "2024-01-03",
     "status": "completed", "amount": 149.99},
    {"id": 4, "user_id": 1, "order_date": "2024-02-01",
     "status": "completed", "amount": 79.99},
    {"id": 5, "user_id": 3, "order_date": "2024-02-15",
     "status": "completed", "amount": 199.99},
    {"id": 6, "user_id": 2, "order_date": "2024-03-01",
     "status": "failed",    "amount": 29.99},
]

print(f"Raw data: {len(raw_customers)} customers, {len(raw_orders)} orders")

# ── Feature Engineering ───────────────────────────────────────
print("\nStep 1: Engineering features...")

def engineer_customer_features(customers, orders):
    features = []

    for customer in customers:
        customer_id = customer['id']

        # get this customer's orders
        customer_orders = [
            o for o in orders
            if o['user_id'] == customer_id
        ]

        # calculate features
        total_orders = len(customer_orders)
        completed_orders = len([
            o for o in customer_orders
            if o['status'] == 'completed'
        ])
        returned_orders = len([
            o for o in customer_orders
            if o['status'] == 'returned'
        ])
        failed_orders = len([
            o for o in customer_orders
            if o['status'] == 'failed'
        ])

        total_spend = sum([
            o['amount'] for o in customer_orders
            if o['status'] == 'completed'
        ])

        avg_order_value = (
            total_spend / completed_orders
            if completed_orders > 0 else 0
        )

        return_rate = (
            returned_orders / total_orders
            if total_orders > 0 else 0
        )

        # days since last order
        if customer_orders:
            last_order_date = max([
                datetime.strptime(o['order_date'], '%Y-%m-%d')
                for o in customer_orders
            ])
            days_since_last_order = (
                datetime(2024, 3, 15) - last_order_date
            ).days
        else:
            days_since_last_order = 999

        # days since signup
        signup_date = datetime.strptime(
            customer['signup_date'], '%Y-%m-%d'
        )
        days_since_signup = (
            datetime(2024, 3, 15) - signup_date
        ).days

        feature_row = {
            "customer_id":              customer_id,
            "feature_timestamp":        datetime.now().isoformat(),
            "total_orders":             total_orders,
            "completed_orders":         completed_orders,
            "returned_orders":          returned_orders,
            "failed_orders":            failed_orders,
            "total_spend":              round(total_spend, 2),
            "avg_order_value":          round(avg_order_value, 2),
            "return_rate":              round(return_rate, 3),
            "days_since_last_order":    days_since_last_order,
            "days_since_signup":        days_since_signup,
            "is_high_value":            total_spend > 200,
            "is_at_risk":               (
                return_rate > 0.3 or
                days_since_last_order > 60
            ),
        }
        features.append(feature_row)

    return features

customer_features = engineer_customer_features(
    raw_customers, raw_orders
)

print(f"Engineered {len(customer_features)} feature rows")
print(f"Features per customer: {len(customer_features[0])}")

# ── Display features ──────────────────────────────────────────
print("\nStep 2: Feature store contents")
print("-" * 60)

for feature in customer_features:
    print(f"\nCustomer {feature['customer_id']}:")
    for key, value in feature.items():
        if key not in ['customer_id', 'feature_timestamp']:
            print(f"  {key:<30} {value}")

# ── Feature validation ────────────────────────────────────────
print("\n\nStep 3: Feature validation")
print("-" * 60)

def validate_features(features):
    issues = []

    for feature in features:
        cid = feature['customer_id']

        # check for nulls
        for key, value in feature.items():
            if value is None:
                issues.append(
                    f"Customer {cid}: null value in {key}"
                )

        # business logic checks
        if feature['return_rate'] < 0 or feature['return_rate'] > 1:
            issues.append(
                f"Customer {cid}: return_rate out of range"
            )

        if feature['avg_order_value'] < 0:
            issues.append(
                f"Customer {cid}: negative avg_order_value"
            )

        if feature['total_orders'] < feature['completed_orders']:
            issues.append(
                f"Customer {cid}: completed > total orders"
            )

    return issues

validation_issues = validate_features(customer_features)

if validation_issues:
    print(f"VALIDATION FAILED — {len(validation_issues)} issues:")
    for issue in validation_issues:
        print(f"  ERROR: {issue}")
else:
    print("All features validated successfully!")
    print(f"  {len(customer_features)} customers")
    print(f"  {len(customer_features[0])} features each")
    print(f"  0 validation issues")

# ── Save features as JSON (simulating feature store) ─────────
print("\n\nStep 4: Saving to feature store")
print("-" * 60)

feature_store = {
    "feature_group": "customer_behaviour",
    "version": "1.0",
    "created_at": datetime.now().isoformat(),
    "feature_count": len(customer_features[0]) - 2,
    "entity_count": len(customer_features),
    "features": customer_features
}

output_path = "customer_features.json"
with open(output_path, 'w') as f:
    json.dump(feature_store, f, indent=2, default=str)

print(f"Feature store saved to {output_path}")
print(f"Feature group: customer_behaviour v1.0")
print(f"Entities: {feature_store['entity_count']} customers")
print(f"Features: {feature_store['feature_count']} per customer")

# ── Simulate model serving ────────────────────────────────────
print("\n\nStep 5: Simulating model serving")
print("-" * 60)

def predict_churn_risk(features):
    score = 0

    if features['days_since_last_order'] > 45:
        score += 3
    elif features['days_since_last_order'] > 30:
        score += 1

    if features['return_rate'] > 0.3:
        score += 2

    if features['total_orders'] == 0:
        score += 3

    if features['failed_orders'] > 0:
        score += 1

    if features['total_spend'] > 200:
        score -= 1

    if score >= 4:
        return "HIGH"
    elif score >= 2:
        return "MEDIUM"
    else:
        return "LOW"

print("Churn Risk Predictions:")
print(f"{'Customer':<12} {'Total Orders':<15} {'Return Rate':<14} {'Days Since Order':<18} {'Risk'}")
print("-" * 70)

for feature in customer_features:
    risk = predict_churn_risk(feature)
    risk_symbol = "🔴" if risk == "HIGH" else "🟡" if risk == "MEDIUM" else "🟢"
    print(
        f"Customer {feature['customer_id']:<3} "
        f"{feature['total_orders']:<15} "
        f"{feature['return_rate']:<14} "
        f"{feature['days_since_last_order']:<18} "
        f"{risk_symbol} {risk}"
    )

print("\n" + "="*60)
print("PIPELINE SUMMARY")
print("="*60)
print(f"""
Raw data:        {len(raw_customers)} customers, {len(raw_orders)} orders
Features:        {len(customer_features[0]) - 2} features engineered per customer
Validation:      {len(validation_issues)} issues found
Feature store:   saved to {output_path}
Predictions:     churn risk scored for all customers

This pipeline mirrors production MLOps:
1. Extract raw data from Snowflake
2. Engineer features (transforms, aggregations, ratios)
3. Validate feature quality before serving
4. Store in feature store with versioning
5. Serve features to model for prediction
""")

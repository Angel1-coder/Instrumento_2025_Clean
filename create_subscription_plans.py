#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import SubscriptionPlan

print("Erstelle Beispiel-Abonnementpläne...")

# Prüfe ob bereits Pläne existieren
existing_plans = SubscriptionPlan.objects.all()
if existing_plans.exists():
    print(f"⚠️ Es existieren bereits {existing_plans.count()} Pläne")
    print("   Überspringe die Erstellung neuer Pläne")
    for plan in existing_plans:
        print(f"   - {plan.name}: €{plan.monthly_price}/Monat ({plan.duration_months} Monate)")
else:
    # Erstelle neue Pläne basierend auf den Frontpage-Preisen
    plans_data = [
        {
            'name': 'Try & Test',
            'duration_months': 3,
            'monthly_price': 199.00,
            'insurance_included': False,
            'lessons_included': False,
            'max_instruments': 1,
            'description': 'Perfekt zum Testen von Instrumenten. Monatliche Kündigung möglich. Grundversicherung inklusive. Keine langfristige Verpflichtung.'
        },
        {
            'name': 'Best Value',
            'duration_months': 6,
            'monthly_price': 179.00,
            'insurance_included': True,
            'lessons_included': True,
            'max_instruments': 1,
            'description': 'Bester Wert! 10% Rabatt gegenüber dem 3-Monats-Plan. 2 Monate kostenlose Unterrichtsstunden. Premium-Versicherung inklusive. Kostenlose Tasche inklusive.'
        },
        {
            'name': 'Serious Musician',
            'duration_months': 12,
            'monthly_price': 159.00,
            'insurance_included': True,
            'lessons_included': True,
            'max_instruments': 2,
            'description': 'Für ernsthafte Musiker! 20% Rabatt gegenüber dem 3-Monats-Plan. 4 Monate kostenlose Unterrichtsstunden. Premium-Versicherung inklusive. Kostenlose Tasche & Zubehör.'
        },
        {
            'name': 'Long-term',
            'duration_months': 24,
            'monthly_price': 139.00,
            'insurance_included': True,
            'lessons_included': True,
            'max_instruments': 3,
            'description': 'Langfristige Option! 30% Rabatt gegenüber dem 3-Monats-Plan. 6 Monate kostenlose Unterrichtsstunden. Premium-Versicherung inklusive. Kostenlose Tasche & Zubehör. VIP-Kundensupport.'
        }
    ]

    for plan_data in plans_data:
        plan = SubscriptionPlan.objects.create(**plan_data)
        print(f"✅ {plan.name} ({plan.duration_months} Monate): €{plan.monthly_price}/Monat")
        print(f"   Versicherung: {'Inklusive' if plan.insurance_included else 'Nicht inklusive'}")
        print(f"   Unterricht: {'Inklusive' if plan.lessons_included else 'Nicht inklusive'}")
        print(f"   Max. Instrumente: {plan.max_instruments}")
        print()

print("\nAbonnementpläne sind bereit!")
print("Sie können sie jetzt unter /products/subscription-plans/ sehen.")
print("Oder besuchen Sie die Homepage für die Übersicht der Mietpläne.")

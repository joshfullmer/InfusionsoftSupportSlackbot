import re


categories = {
    'admin': ['admin', 'deactivate'],
    'api': ['api', '3rd party', 'third party', 'plugin', 'integrate', 'integration'],
    'app data': ['block', 'server'],
    'billing ar': ['pricing'],
    'broadcast': ['broadcast'],
    'campaign': ['campaign', 'timer', 'sequence', 'goal', 'decision diamond', 'decision node', 'merge field', 'landing page'],
    'contact': ['contact search'],
    'crm': ['task', 'note', 'appointment', 'company', 'companies'],
    'customerhub': ['customerhub'],
    'dashboard': ['dashboard', 'my day', 'widget'],
    'data cleanup': ['dup', 'dupe', 'duplicate', 'modify', 'contact merge', 'merge contact'],
    'e-commerce setup': ['order form', 'shopping cart', 'discount', 'upsell', 'checkout', 'promo code', 'promotion'],
    'e-commerce': ['order', 'subscription', 'payment', 'e-commerce', 'ecommerce', 'ecom', 'paypal', 'auth.net', 'product', 'invoice', 'quote', 'payflow pro', 'tax'],
    'email hygiene': ['optin', 'opt in', 'opt-in', 'optout', 'opt out', 'opt-out', 'domain', 'engaged', 'unengaged', 'bounce'],
    'email plugin': ['outlook', 'gmail', 'sync'],
    'import/export': ['import', 'export', 'csv', 'restricted'],
    'marketing': ['email template'],
    'new infusionsoft': ['nis', 'new infusionsoft'],
    'opportunity': ['opportunity', 'opportunities', 'pipeline', 'stage', 'card', 'deal'],
    'performance': ['slowness', 'performance', 'chrome', 'firefox', 'safari'],
    'referral partners': ['referral partner', 'affiliate', 'commission', 'clawback', 'tracking link', 'partner portal', 'partner center'],
    'reports': ['report'],
    'settings': ['setting'],
    'user permissions': ['permissions'],
    'users': ['user', 'login', 'signature', 'infusionsoft id'],
    'wepay': ['is payments', 'isp', 'wepay', 'infusionsoft payments', 'chargeback'],
}


def categorize(message):
    message_cats = set()

    # Remove links and user mentions from categorization
    message = re.sub(r'<.*?>', '', message)
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in message.lower():
                message_cats.add(category)
    if not message_cats:
        return None
    return ','.join(message_cats)

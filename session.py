class SessionUser:
    def __init__(self):
        # Identity
        self.first_name = None
        self.last_name = None
        self.email = None
        self.platform = None
        self.plan = None
        self.awaiting_slot = None

        # Intent flags (NOT modes)
        self.wants_info = False
        self.wants_pricing = False
        self.wants_to_buy = False

        # Lifecycle
        self.lead_submitted = False

    def is_complete(self) -> bool:
        """All required lead fields collected"""
        return all([
            self.first_name,
            self.email,
            self.platform,
            self.plan
        ])

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "platform": self.platform,
            "plan": self.plan,
            "wants_info": self.wants_info,
            "wants_pricing": self.wants_pricing,
            "wants_to_buy": self.wants_to_buy,
            "lead_submitted": self.lead_submitted
        }

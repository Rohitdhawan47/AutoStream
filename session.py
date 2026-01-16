class SessionUser:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.platform = None
        self.mode = "chat"
        self.lead_submitted = False
        self.plan = None
    
    def is_complete(self)->bool:
        return (
            self.first_name is not None
            and self.email is not None
            and self.platform is not None
            and self.plan is not None
        )
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "platform": self.platform,
            "mode": self.mode,
            "lead_submitted": self.lead_submitted
        }
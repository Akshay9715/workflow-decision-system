import random


class CreditScoreService:

    def get_credit_score(self, user_data):

        # simulate failure 30% of the time
        if random.random() < 0.3:
            raise Exception("Credit service unavailable")

        return user_data.get("credit_score", 0)
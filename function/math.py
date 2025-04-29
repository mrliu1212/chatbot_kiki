class Calculator:
    @staticmethod
    def calculate_duration(interest, face_value, time, coupon_rate):
        try:
            coupon = face_value * coupon_rate
            numerator = sum((1 + i) * coupon / (1 + interest) ** (1 + i) for i in range(time - 1)) + time * (coupon + face_value)/(1 + interest)
            denominator = sum(coupon / (1 + interest) ** (1 + i) for i in range(time - 1)) + (coupon + face_value)/(1 + interest)            

            duration = numerator / denominator
            return duration
        except ValueError:
            return False

    @staticmethod
    def calculate_npv(initial_investment, time, cost_capital, cash_flow):
        try:            
            npv = sum(cash_flow[i] / (1 + cost_capital) ** (i + 1) for i in range(time)) - initial_investment
            return npv
        except ValueError:
            return False

    @staticmethod
    def calculate_fv(interest, time, pv):
        try:
            fv = pv * (1 + interest) ** time
            return fv
        except ValueError:
            return False



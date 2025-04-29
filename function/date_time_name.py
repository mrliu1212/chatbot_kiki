class DateTimeName:
    # TODO language
    @staticmethod
    def get_month(month):
        """
        Static method to get the month name based on its numerical representation.

        Args:
            month (int): Numeric representation of the month (1 to 12).

        Returns:
            str: Full name of the month.

        """
        # List of month names
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        # Iterate through months and return the corresponding name
        for i, m in enumerate(months):
            if month == i + 1:
                return m

    @staticmethod
    def get_weekday(day):
        """
        Static method to get the weekday name based on its numerical representation.

        Args:
            day (int): Numeric representation of the weekday (1 to 7).

        Returns:
            str: Full name of the weekday.

        """
        # List of weekday names
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Iterate through weekdays and return the corresponding name
        for i, d in enumerate(week):
            if day == i + 1:
                return d

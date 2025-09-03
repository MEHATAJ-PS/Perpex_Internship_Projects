import time

class RateLimiter:
    def __init__(self, max_requests, time_window):
        """
        Initialize the RateLimiter.
        :param max_requests: Maximum requests allowed in the given time window.
        :param time_window: Time window in seconds.
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests = {}  # {user_id: [timestamps]}

    def allow_request(self, user_id):
        """
        Determines whether a request is allowed for a user.
        :param user_id: Unique identifier for the user.
        :return: True if request is allowed, False if blocked.
        """
        current_time = time.time()

        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        # Keep only requests within the current time window
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id]
            if current_time - t < self.time_window
        ]

        if len(self.user_requests[user_id]) < self.max_requests:
            self.user_requests[user_id].append(current_time)
            return True
        else:
            return False


if __name__ == "__main__":
    # Example usage
    limiter = RateLimiter(max_requests=3, time_window=10)  # 3 requests per 10 seconds
    user = "user_123"

    print("Simulating 5 requests with 2 seconds delay...\n")
    for i in range(5):
        if limiter.allow_request(user):
            print(f"Request {i+1}: ✅ Allowed")
        else:
            print(f"Request {i+1}: ❌ Blocked - Rate limit exceeded")
        time.sleep(2)

    print("\nWaiting 10 seconds for rate limit reset...\n")
    time.sleep(10)

    for i in range(2):
        if limiter.allow_request(user):
            print(f"Request after reset {i+1}: ✅ Allowed")
        else:
            print(f"Request after reset {i+1}: ❌ Blocked")

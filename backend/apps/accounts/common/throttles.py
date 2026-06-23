from rest_framework.throttling import AnonRateThrottle


class RegistrationRateThrottle(AnonRateThrottle):
    """Limit anonymous account registration attempts by origin."""

    scope = "users_registration"

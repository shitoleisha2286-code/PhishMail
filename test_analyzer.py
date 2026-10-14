
import unittest
from analyzer import analyze_email


class TestPhishMail(unittest.TestCase):

    def test_suspicious_phrase(self):
        warnings, score, level = analyze_email(
            "Account suspended",
            "Please verify your password."
        )

        self.assertGreater(score, 0)
        self.assertTrue(
            any(w["type"] == "Suspicious phrase" for w in warnings)
        )

    def test_http_link(self):
        warnings, score, level = analyze_email(
            "Website information",
            "Visit http://example.com"
        )

        self.assertTrue(
            any(w["type"] == "Unencrypted HTTP link" for w in warnings)
        )

    def test_url_shortener(self):
        warnings, score, level = analyze_email(
            "Prize notification",
            "Claim your reward at https://bit.ly/example"
        )

        self.assertTrue(
            any(w["type"] == "URL shortener" for w in warnings)
        )

    def test_ip_address_url(self):
        warnings, score, level = analyze_email(
            "Website notice",
            "Visit http://192.168.1.10/login"
        )

        self.assertTrue(
            any(
                w["type"] == "IP address used as website"
                for w in warnings
            )
        )

    def test_normal_email(self):
        warnings, score, level = analyze_email(
            "Team meeting tomorrow",
            "Our project meeting starts at 10 AM. See you there!"
        )

        self.assertEqual(warnings, [])
        self.assertEqual(score, 0)
        self.assertEqual(level, "Low")

    def test_score_never_exceeds_100(self):
        warnings, score, level = analyze_email(
            "URGENT: Account suspended",
            (
                "Verify your password. Confirm your OTP. "
                "Click here immediately: "
                "http://192.168.1.10/login "
                "https://bit.ly/example"
            )
        )

        self.assertLessEqual(score, 100)
        self.assertGreaterEqual(score, 0)


if __name__ == "__main__":
    unittest.main()

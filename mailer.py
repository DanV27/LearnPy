"""
Outbound transactional email — currently console-only.

send_email() is the seam a real provider plugs into later: once
EMAIL_API_KEY is set in the environment, replace the body of this
function with a call to that provider's API (e.g. Resend's
`resend.Emails.send(...)`). Every caller in the app already goes through
this function, so wiring up a provider is a one-file change.

Until then, every "sent" email is just printed to the console in a loud,
hard-to-miss block — handy for local dev and for the forgot-password flow,
where the reset link would otherwise go nowhere.
"""
import os


def send_email(to: str, subject: str, body: str) -> None:
    """"Send" an email. Console mode unless EMAIL_API_KEY is configured."""
    if not os.environ.get("EMAIL_API_KEY"):
        _print_console(to, subject, body)
        return

    # TODO: EMAIL_API_KEY is set — plug in the real provider here, e.g.:
    #   import resend
    #   resend.api_key = os.environ["EMAIL_API_KEY"]
    #   resend.Emails.send({"from": "...", "to": to, "subject": subject, "text": body})
    # Until that's wired up, fall back to console mode so nothing is lost.
    _print_console(to, subject, body)


def _print_console(to: str, subject: str, body: str) -> None:
    border = "=" * 72
    # flush=True: stdout is block-buffered when it's not a TTY (e.g. piped
    # to a log file or process manager), which would otherwise leave the
    # reset link sitting invisibly in a buffer instead of showing up.
    print(f"\n{border}", flush=True)
    print("EMAIL (console mode — no EMAIL_API_KEY configured)", flush=True)
    print(border, flush=True)
    print(f"To:      {to}", flush=True)
    print(f"Subject: {subject}", flush=True)
    print(border, flush=True)
    print(body, flush=True)
    print(f"{border}\n", flush=True)

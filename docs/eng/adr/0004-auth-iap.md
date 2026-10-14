# ADR-0004: Auth: Google sign-in via IAP, single allow-listed account
- **Status:** Proposed (M3)
- **Decision:** Put Identity-Aware Proxy in front of the Cloud Run service, allowing only Ayush's Google account. The app reads the IAP identity header to get the `user_id`.
- **Why:** No auth code to write, strong security, and it fits "single user now, more later" (add accounts to the allow-list).
- **To verify:** Direct IAP support on Cloud Run. Fallbacks: an HTTPS load balancer with IAP (adds cost), or in-app Google Sign-In with an allow-list.

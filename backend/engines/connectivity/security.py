from typing import Dict, List


class ConnectivitySecurity:
    """Connectivity security assessment service."""

    def assess(
        self,
        internet: bool,
        wifi: bool,
        ethernet: bool,
        hotspot: bool,
        vpn: bool,
        current_network: str = None,
        network_security: str = "UNKNOWN",
    ) -> Dict[str, object]:
        """Assess connectivity security using available evidence."""

        checks: List[Dict[str, object]] = []
        warnings: List[str] = []

        if wifi:
            checks.append(
                {
                    "check": "wifi",
                    "status": "DETECTED",
                }
            )

        if ethernet:
            checks.append(
                {
                    "check": "ethernet",
                    "status": "DETECTED",
                }
            )

        if hotspot:
            checks.append(
                {
                    "check": "hotspot",
                    "status": "DETECTED",
                }
            )
            warnings.append(
                "Mobile or personal hotspot connectivity detected."
            )

        if vpn:
            checks.append(
                {
                    "check": "vpn",
                    "status": "DETECTED",
                }
            )

        if current_network:
            checks.append(
                {
                    "check": "current_network",
                    "status": "DETECTED",
                    "network": current_network,
                }
            )

        normalized_security = (
            network_security or "UNKNOWN"
        ).upper()

        if normalized_security in {
            "OPEN",
            "NONE",
            "UNSECURED",
        }:
            warnings.append(
                "The detected wireless network appears "
                "to have no authentication."
            )

            security = "UNSAFE"

        elif normalized_security in {
            "WPA3",
            "WPA2",
            "WPA2-PERSONAL",
            "WPA3-PERSONAL",
        }:
            security = "SECURE"

        elif normalized_security == "UNKNOWN":
            security = "UNKNOWN"

        else:
            security = "WARNING"

        checks.append(
            {
                "check": "network_security",
                "status": normalized_security,
            }
        )

        if not internet:
            checks.append(
                {
                    "check": "internet",
                    "status": "OFFLINE",
                }
            )

            if security == "SECURE":
                security = "WARNING"

            warnings.append(
                "External Internet connectivity is unavailable."
            )

        else:
            checks.append(
                {
                    "check": "internet",
                    "status": "ONLINE",
                }
            )

        if security == "UNSAFE":
            overall = "UNSAFE"
        elif security == "WARNING" or warnings:
            overall = "WARNING"
        elif security == "SECURE":
            overall = "SECURE"
        else:
            overall = "UNKNOWN"

        return {
            "security": overall,
            "network_security": normalized_security,
            "warnings": warnings,
            "checks": checks,
        }

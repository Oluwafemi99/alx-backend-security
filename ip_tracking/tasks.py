from celery import shared_task
from django.utils.timezone import now, timedelta
from ip_tracking.models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']


@shared_task
def flag_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)

    # Get all logs from the past hour
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    flagged_ips = set()

    for log in recent_logs:
        ip = log.ip_address
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Check for sensitive path access
        if log.path in SENSITIVE_PATHS:
            flagged_ips.add(ip)
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Accessed sensitive path: {log.path}"}
            )

    # Flag IPs exceeding 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100 and ip not in flagged_ips:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"{count} requests in the past hour"}
            )

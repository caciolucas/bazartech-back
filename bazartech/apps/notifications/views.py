from django.http import HttpResponse
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice


# Create your views here.

def test_notification(request):
    # You can still use .filter() or any methods that return QuerySet (from the chain)
    device = FCMDevice.objects.all().first()
    # send_message parameters include: message, dry_run, app
    device.send_message(
        Message(
            data={
                "body": "great match!",
                "Room": "PortugalVSDenmark"
            },
        )
                )

    return HttpResponse("Success")

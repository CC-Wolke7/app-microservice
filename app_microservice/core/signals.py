from .bucket import delete_image
from .models import OfferImage
from .publisher import notify_offer_created


def delete_offer_images(sender, instance, using, **kwargs):
    offer = instance

    for image in OfferImage.objects.filter(offer=offer):
        try:
            delete_image(image.name)
        except:  # noqa
            pass

        image.delete()


def send_offer_created_notification(sender, instance, using, **kwargs):
    offer = instance
    notify_offer_created(offer)

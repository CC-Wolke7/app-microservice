from core.bucket import delete_image

from .models import OfferImage


def delete_offer_images(sender, instance, using, **kwargs):
    for image in OfferImage.objects.filter(offer=instance):
        try:
            delete_image(image.name)
        except:  # noqa
            pass

        image.delete()

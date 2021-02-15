import base64
import json
import mimetypes
import os
from typing import Callable, List, Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from core.bucket import delete_image, upload_image
from core.choices import Breed, Sex, Species
from core.models import Offer, OfferImage, User

DATA_DIRECTORY = os.path.join(settings.BASE_DIR, "core", "management", "data")


class FileNotFoundError(Exception):
    pass


class Command(BaseCommand):
    help = "Fill database with demo users and offers"

    # Files should be put in adjacent `data` directory:
    #     - `data.json`
    #     - `offers.json`

    def add_arguments(self, parser):
        parser.add_argument(
            '--remove',
            action='store_true',
            help='Remove the demo entries',
        )

    def handle(self, *args, **options):
        if options['remove']:
            User.objects.filter(demo_id__isnull=False
                                ).delete()  # cascade delete
            return

        self.import_users(**options)
        self.import_offers(**options)

    def import_users(self, **options):
        path = os.path.join(DATA_DIRECTORY, "users.json")

        if not os.path.exists(path):
            self.stdout.write(f"Could not find demo users file: {path}")
            return

        self.stdout.write("Creating demo users...")
        entries = self.parse_users_json(path)
        self.import_models(User, entries, **options)
        self.stdout.write("\n")

    def import_offers(self, **options):
        path = os.path.join(DATA_DIRECTORY, "offers.json")

        if not os.path.exists(path):
            self.stdout.write(f"Could not find demo offers file: {path}")
            return

        self.stdout.write("Creating demo offers...")
        entries = self.parse_offers_json(path)
        self.import_models(Offer, entries, **options)
        self.stdout.write("\n")

        self.stdout.write("Uploading offer images...")
        self.import_offer_images(path)

    def import_offer_images(self, path: str):
        with open(path) as json_file:
            offers = json.load(json_file)

            for demo_offer in offers:
                demo_offer_id = demo_offer.pop("id")

                try:
                    stored_offer = Offer.objects.get(demo_id=demo_offer_id)
                except Offer.DoesNotExist:
                    continue

                image_name: str = demo_offer.pop("image")
                image_path = os.path.join(DATA_DIRECTORY, "images", image_name)
                image = self.file_to_data_uri(image_path)

                stored_image_name = (
                    f"{str(stored_offer.uuid)}_offer_image_{image_name}"
                )

                upload_image(stored_image_name, image)

                try:
                    OfferImage.objects.create(
                        offer=stored_offer, name=stored_image_name
                    )

                    self.stdout.write(
                        self.style.SUCCESS((
                            f"Uploaded image for demo offer '{demo_offer_id}'."  # noqa
                        ))
                    )
                except IntegrityError:
                    delete_image(stored_image_name)

                    self.stdout.write(
                        self.style.NOTICE(
                            f"Image for demo offer '{demo_offer_id}' already exists."  # noqa
                        )
                    )

    def import_models(self, Model, entries: List, **options):
        with transaction.atomic():
            initial_count = Model.objects.count()

            Model.objects.bulk_create(
                entries,
                ignore_conflicts=True,
                batch_size=1000,
            )

            final_count = Model.objects.count()

        created = final_count - initial_count
        conflicts = len(entries) - created

        self.stdout.write(
            "\n".join([
                self.style.HTTP_INFO(f"Parsed {len(entries)} JSON entries."),
                self.style.SUCCESS(f"{created} records created.")
            ])
        )

        if conflicts:
            self.stdout.write(
                self.style.NOTICE(f"Ignored {conflicts} conflicting records.")
            )

    def parse_users_json(self, path: str):
        def user_kwargs(item: dict) -> dict:
            return dict(
                demo_id=item.pop("id"),
                name=item.pop("name"),
                email=item.pop("email"),
            )

        return self.parse_json(path, User, user_kwargs)

    def parse_offers_json(self, path: str):
        def offer_kwargs(item: dict) -> Optional[dict]:
            # Get user
            try:
                user = User.objects.get(demo_id=item.pop("sellerId"))
            except User.DoesNotExist:
                return None

            # Parse to Species
            species_str: str = item.pop("species")
            species = Species(species_str)

            # Parse to Breed
            breed_str: str = item.pop("breed")
            breed = Breed(breed_str)

            # Parse to Sex
            sex_str: str = item.pop("sex")
            sex = Sex(sex_str)

            return dict(
                demo_id=item.pop("id"),
                published_by=user,
                name=item.pop("name"),
                age=item.pop("age"),
                species=species,
                breed=breed,
                sex=sex,
                location=item.pop("location"),
                description=item.pop("description")
            )

        return self.parse_json(path, Offer, offer_kwargs)

    def parse_json(
        self, path: str, Model, model_kwargs: Callable[[dict], Optional[dict]]
    ):
        entries = []

        with open(path) as json_file:
            data = json.load(json_file)

            for item in data:
                kwargs = model_kwargs(item)

                if kwargs is None:
                    continue

                model = Model(**kwargs)
                entries.append(model)

        return entries

    def file_to_data_uri(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError

        mime, _ = mimetypes.guess_type(path)

        with open(path, 'rb') as file:
            data = file.read()
            data64 = base64.b64encode(data).decode()

            return u'data:%s;base64,%s' % (mime, data64)

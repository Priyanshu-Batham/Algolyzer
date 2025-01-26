import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Dump data for quiz models (Question and Topic) into a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="./data/quiz_data.json",
            help="Output file path (default: ./data/quiz_data.json)",
        )

    def handle(self, *args, **kwargs):
        output_path = kwargs["output"]
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.stdout.write("Dumping quiz data into: {}".format(output_path))

        call_command(
            "dumpdata",
            "quiz.Question",
            "quiz.Topic",
            "--natural-primary",
            "--natural-foreign",
            "--indent",
            "4",
            stdout=open(output_path, "w"),
        )

        self.stdout.write(self.style.SUCCESS("Data dumped successfully!"))

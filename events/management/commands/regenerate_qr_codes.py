from django.core.management.base import BaseCommand
from events.models import Event


class Command(BaseCommand):
    help = 'Regenerate QR codes for events that are missing them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Regenerate QR codes for all events (not just missing ones)',
        )
        parser.add_argument(
            '--event-id',
            type=int,
            help='Regenerate QR code for a specific event ID',
        )

    def handle(self, *args, **options):
        if options['event_id']:
            # Regenerate for specific event
            try:
                event = Event.objects.get(pk=options['event_id'])
                event.generate_qr_code()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully regenerated QR code for event: {event.title}')
                )
            except Event.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Event with ID {options["event_id"]} not found')
                )
            return

        # Get events that need QR codes
        if options['all']:
            events = Event.objects.all()
            self.stdout.write('Regenerating QR codes for all events...')
        else:
            events = Event.objects.filter(qr_code='')
            self.stdout.write('Regenerating QR codes for events missing QR codes...')

        count = 0
        errors = 0

        for event in events:
            try:
                event.generate_qr_code()
                count += 1
                self.stdout.write(f'✓ Generated QR code for: {event.title}')
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to generate QR code for {event.title}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Generated QR codes for {count} events. {errors} errors.'
            )
        )

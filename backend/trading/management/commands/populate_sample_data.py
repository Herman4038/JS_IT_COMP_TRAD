# Add your custom management commands here
from django.core.management.base import BaseCommand
from backend.trading.models import Inventory
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample inventory data'
    
    def handle(self, *args, **options):
        # Sample inventory items
        sample_items = [
            {
                'item_name': 'Gaming Laptop',
                'brand': 'ASUS',
                'model': 'ROG Strix G15',
                'description': 'High-performance gaming laptop with RTX 3060 graphics',
                'unit_cost': Decimal('45000.00'),
                'srp_price': Decimal('55000.00'),
                'quantity': 5,
                'serial_number': 'ASUS-ROG-001'
            },
            {
                'item_name': 'Wireless Mouse',
                'brand': 'Logitech',
                'model': 'G Pro X Superlight',
                'description': 'Ultra-lightweight wireless gaming mouse',
                'unit_cost': Decimal('2500.00'),
                'srp_price': Decimal('3500.00'),
                'quantity': 15,
                'serial_number': 'LOG-GPX-001'
            },
            {
                'item_name': 'Mechanical Keyboard',
                'brand': 'Corsair',
                'model': 'K100 RGB',
                'description': 'Premium mechanical gaming keyboard with RGB lighting',
                'unit_cost': Decimal('8000.00'),
                'srp_price': Decimal('12000.00'),
                'quantity': 8,
                'serial_number': 'COR-K100-001'
            },
            {
                'item_name': 'Gaming Headset',
                'brand': 'SteelSeries',
                'model': 'Arctis Pro',
                'description': 'High-fidelity gaming headset with clear cast microphone',
                'unit_cost': Decimal('3500.00'),
                'srp_price': Decimal('5000.00'),
                'quantity': 12,
                'serial_number': 'STE-AP-001'
            },
            {
                'item_name': 'Gaming Monitor',
                'brand': 'AOC',
                'model': '24G2',
                'description': '24-inch 144Hz gaming monitor with IPS panel',
                'unit_cost': Decimal('12000.00'),
                'srp_price': Decimal('18000.00'),
                'quantity': 3,
                'serial_number': 'AOC-24G2-001'
            },
            {
                'item_name': 'Gaming Chair',
                'brand': 'DXRacer',
                'model': 'Formula Series',
                'description': 'Ergonomic gaming chair with lumbar support',
                'unit_cost': Decimal('15000.00'),
                'srp_price': Decimal('22000.00'),
                'quantity': 2,
                'serial_number': 'DXR-FS-001'
            },
            {
                'item_name': 'Gaming Mousepad',
                'brand': 'Razer',
                'model': 'Goliathus Extended',
                'description': 'Large gaming mousepad with RGB lighting',
                'unit_cost': Decimal('800.00'),
                'srp_price': Decimal('1500.00'),
                'quantity': 20,
                'serial_number': 'RAZ-GOL-001'
            },
            {
                'item_name': 'Gaming Microphone',
                'brand': 'Blue',
                'model': 'Yeti X',
                'description': 'Professional USB condenser microphone',
                'unit_cost': Decimal('5000.00'),
                'srp_price': Decimal('7500.00'),
                'quantity': 6,
                'serial_number': 'BLU-YETI-001'
            },
            {
                'item_name': 'Gaming Webcam',
                'brand': 'Logitech',
                'model': 'C922 Pro Stream',
                'description': '1080p streaming webcam with background replacement',
                'unit_cost': Decimal('3000.00'),
                'srp_price': Decimal('4500.00'),
                'quantity': 10,
                'serial_number': 'LOG-C922-001'
            },
            {
                'item_name': 'Gaming Controller',
                'brand': 'Xbox',
                'model': 'Elite Series 2',
                'description': 'Premium wireless gaming controller with customizable buttons',
                'unit_cost': Decimal('6000.00'),
                'srp_price': Decimal('9000.00'),
                'quantity': 4,
                'serial_number': 'XBOX-ELITE-001'
            }
        ]
        
        # Create inventory items
        created_count = 0
        for item_data in sample_items:
            item, created = Inventory.objects.get_or_create(
                serial_number=item_data['serial_number'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {item.item_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Skipped (exists): {item.item_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} inventory items')
        ) 
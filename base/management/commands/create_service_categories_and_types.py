from django.core.management.base import BaseCommand
from base.views import services
from base.models import ServiceCategory as SC, ServiceType as ST
from decimal import Decimal


class Command(BaseCommand):
    help = """Create Service Categories and Specific Service Type Options under each service category.
        \rThe values for creating these objects are obtained from the servise structure in base.views"""
    
    def handle(self, *args, **options):
        for s in services:
            service_cat = SC.objects.create(
                title=s.get('title'),
                description=s.get('desc'),
                fee=s.get('fee'),
                temp=s.get('temp'),
                has_sep_temp=bool(s.get('septemp')),
                require_file_uploads = bool(s.get('file_upload')),
                require_payment = bool(s.get('payment_required')),
                form_hidden_first=bool(s.get('hidden_first'))
            )
            if "items" in s.keys():
                for item in s['items']:
                    fee = None
                    if isinstance(item, str):
                        st_desc = item
                    elif isinstance(item, dict):
                        if "procurement" not in s['title'].lower():
                            st_desc = item['text']
                            fee = Decimal(item['fee']) if "consultancy" in s['title'].lower() else None
                        elif 'procurement' in s['title'].lower():
                            st_desc = item['desc']
                            fee = Decimal(item['tot_fee'])
                    service_type = ST.objects.create(
                        description=st_desc,
                        service_category =service_cat,
                        fee=fee
                    )
                    self.stdout.write(self.style.SUCCESS(f"Successfully Created: {st_desc} \nService Category : {service_cat.title}\n\n"))
            else:
                 self.stdout.write(self.style.SUCCESS(f"Successfully a Service Category with no subservices\nService Category : {service_cat.title}\n\n"))






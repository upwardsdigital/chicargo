
from django.utils.deprecation import MiddlewareMixin
from orders.models import PaymentStatus

from .models import Truck


class SetTruckPaymentStatusMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        trucks = Truck.objects.all()
        for truck in trucks:
            if sum(
                    [
                        truck_payment.amount for truck_payment in truck.truck_payments.all()
                    ]
            ) >= truck.payment_amount:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="paid",
                    defaults={'name': 'Оплачено'}
                )
                truck.payment_status = payment_status
            elif sum(
                    [
                        truck_payment.amount for truck_payment in truck.truck_payments.all()
                    ]
            ) < truck.payment_amount and sum(
                    [
                        truck_payment.amount for truck_payment in truck.truck_payments.all()
                    ]
            ) != 0:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="partially",
                    defaults={'name': 'Оплачен частично'}
                )
                truck.payment_status = payment_status
            else:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="not_paid",
                    defaults={'name': 'Не оплачено'}
                )
                truck.payment_status = payment_status
            truck.save()

        return response

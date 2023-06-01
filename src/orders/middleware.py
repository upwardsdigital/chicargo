from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from .models import Product, PaymentStatus


class SetPaymentStatusMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        products = Product.objects.all()
        for product in products:
            if sum(
                    [
                        payment.amount for payment in product.payments.all()
                    ]
            ) >= product.price:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="paid",
                    defaults={'name': 'Оплачено'}
                )
                product.payment_status = payment_status
            elif sum(
                    [
                        payment.amount for payment in product.payments.all()
                    ]
            ) < product.price and sum(
                    [
                        payment.amount for payment in product.payments.all()
                    ]
            ) != 0:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="partially",
                    defaults={'name': 'Оплачен частично'}
                )
                product.payment_status = payment_status
            else:
                payment_status, _ = PaymentStatus.objects.get_or_create(
                    slug="not_paid",
                    defaults={'name': 'Не оплачено'}
                )
                product.payment_status = payment_status
            product.save()

        return response

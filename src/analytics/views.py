from rest_framework import views, response, status
import pandas as pd
from datetime import datetime, timedelta
from orders.models import Product
from expenses.models import Expense
from trucks.models import Truck


class AnalyticsAPIView(views.APIView):

    def post(self, request):
        start_date = request.data.get("start_date", None)
        end_date = request.data.get("end_date", None)
        freq = request.data.get("flag", "D")
        list_of_products_money = list()
        list_of_expenses_money = list()
        list_of_trucks_money = list()
        if start_date is not None and end_date is not None:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")
            total_products_price = sum([
                product.price for product in
                Product.objects.all()
            ])
            total_expenses = sum([
                expense.amount for expense in
                Expense.objects.all()
            ])
            total_trucks_payment = sum([
                truck.payment_amount for truck in
                Truck.objects.all()
            ])
            date_range = pd.date_range(
                start=start_date, end=end_date, freq=freq
            ).tolist()
            for date in date_range:
                list_of_products_money.append(
                    sum(
                        [product.price
                         for product in Product.objects.filter(
                            created_at__gte=start_date,
                            created_at__lte=date
                        )]
                    )
                )
                list_of_expenses_money.append(
                    sum(
                        [expense.amount
                         for expense in Expense.objects.filter(
                            date__gte=start_date,
                            date__lte=date
                        )]
                    )
                )
                list_of_trucks_money.append(
                    sum(
                        [truck.payment_amount
                         for truck in Truck.objects.filter(
                            created_at__gte=start_date,
                            created_at__lte=date
                        )]
                    )
                )

            return response.Response(
                {
                    "total_products_price": total_products_price,
                    "total_expenses": total_expenses,
                    "total_trucks_payment": total_trucks_payment,
                    "labels": date_range,
                    "chart_data_products": list_of_products_money,
                    "chart_data_expenses": list_of_expenses_money,
                    "chart_data_trucks": list_of_trucks_money
                }, status=status.HTTP_200_OK
            )
        return response.Response(
            {
                "total_products_price": 0,
                "total_expenses": 0,
                "total_trucks_payment": 0,
                "labels": [],
                "chart_data_products": [],
                "chart_data_expenses": [],
                "chart_data_trucks": []
            }, status=status.HTTP_200_OK
        )

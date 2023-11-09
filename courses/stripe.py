import stripe

from rest_framework import status
from rest_framework.response import Response

from config import settings
from courses.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def create_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
    )
    return customer


def create_product(course):
    product = stripe.Product.create(name=course.title)
    return product


def create_price(course):
    price = stripe.Price.create(
        unit_amount=course.price,
        currency=course.currency,
        product=create_product(course.title).id,
    )
    return price.id


def create_intent(request):
    intent = stripe.PaymentIntent.create(
        amount=request.data['total_paid'],
        currency=request.data['currency'],
        customer=create_customer(request.user)
    )
    return Response(status=status.HTTP_200_OK, data={"intent": intent})


def get_intent(pk):
    try:
        payment_intent_id = Payment.objects.get(pk=pk).stripe_id
        payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent_id
        )
        return Response(status=status.HTTP_200_OK, data=payment_intent)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


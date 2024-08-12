from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(order):
    subject = 'Order Confirmation'
    message = f'''
    Dear {order.user.username},

    Thank you for your order!

    Order Details:
    Product: {order.product}
    Quantity: {order.quantity}
    Total Price: {order.total_price}

    We will process your order soon.

    Best regards,
    Your Company
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email]

    send_mail(subject, message, from_email, recipient_list)

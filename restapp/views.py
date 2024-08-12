from rest_framework import viewsets
from .models import Product, Review, UserCart, CartItem,Order
from .serializers import ProductSerializer, ReviewSerializer, UserCartSerializer, CartItemSerializer,OrderSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import send_order_confirmation_email
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import pkg_resources
import razorpay
import json
from razorpay.errors import GatewayError,BadRequestError,ServerError
from razorpay import Client
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductsVirtualViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class UserCartViewSet(viewsets.ModelViewSet):
    queryset = UserCart.objects.all()
    serializer_class = UserCartSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        send_order_confirmation_email(order)
        

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
#     permission_classes = [IsAuthenticated]
    

class SendEmailView(APIView):
    def post(self, request):
        subject = 'Test Email '
        message = 'This is a test email sent from Happy Couple Solutions.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['vipinrajk026@gmail.com']

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "Test email sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            




class CreateRazorpayOrderView(APIView):
    def post(self, request):
        try:
            price = request.data.get('price')
            if not price:
                return Response({'error': 'Price is required'}, status=status.HTTP_400_BAD_REQUEST)

            client = self.get_razorpay_client()
            order_amount = int(price) * 100  # Ensure price is an integer
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'

            order = client.order.create({
                'amount': order_amount,
                'currency': order_currency,
                'receipt': order_receipt,
                'payment_capture': '1'
            })

            return Response({'order_id': order['id']}, status=status.HTTP_201_CREATED)
        except BadRequestError as e:
            return Response({'error': 'Bad request: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except GatewayError as e:
            return Response({'error': 'Gateway error: ' + str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except ServerError as e:
            return Response({'error': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_razorpay_client(self):
        razorpay_key_id = os.environ.get('RAZORPAY_KEY_ID')
        razorpay_key_secret = os.environ.get('RAZORPAY_KEY_SECRET')
        if not razorpay_key_id or not razorpay_key_secret:
            raise EnvironmentError("Razorpay environment variables not set")
        return Client(auth=(razorpay_key_id, razorpay_key_secret))

class CaptureRazorpayPaymentView(APIView):
    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            price = request.data.get('price')
            if not payment_id or not price:
                return Response({'error': 'Payment ID and price are required'}, status=status.HTTP_400_BAD_REQUEST)

            client = self.get_razorpay_client()
            amount = int(price) * 100  # Ensure price is an integer

            capture = client.payment.capture(payment_id, amount)
            return Response({'capture_id': capture['id']}, status=status.HTTP_200_OK)
        except BadRequestError as e:
            return Response({'error': 'Bad request: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except GatewayError as e:
            return Response({'error': 'Gateway error: ' + str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except ServerError as e:
            return Response({'error': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_razorpay_client(self):
        razorpay_key_id = os.environ.get('RAZORPAY_KEY_ID')
        razorpay_key_secret = os.environ.get('RAZORPAY_KEY_SECRET')
        if not razorpay_key_id or not razorpay_key_secret:
            raise EnvironmentError("Razorpay environment variables not set")
        return Client(auth=(razorpay_key_id, razorpay_key_secret))

class RefundRazorpayPaymentView(APIView):
    def post(self, request):
        try:
            payment_id = request.data.get('payment_id')
            price = request.data.get('price')
            if not payment_id or not price:
                return Response({'error': 'Payment ID and amount are required'}, status=status.HTTP_400_BAD_REQUEST)

            client = self.get_razorpay_client()
            refund_amount = int(price) * 100  # Ensure amount is in paise

            refund = client.payment.refund(payment_id, {
                'amount': refund_amount
            })

            return Response({'refund_id': refund['id']}, status=status.HTTP_200_OK)
        except BadRequestError as e:
            return Response({'error': 'Bad request: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except GatewayError as e:
            return Response({'error': 'Gateway error: ' + str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except ServerError as e:
            return Response({'error': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_razorpay_client(self):
        razorpay_key_id = os.environ.get('RAZORPAY_KEY_ID')
        razorpay_key_secret = os.environ.get('RAZORPAY_KEY_SECRET')
        if not razorpay_key_id or not razorpay_key_secret:
            raise EnvironmentError("Razorpay environment variables not set")
        return Client(auth=(razorpay_key_id, razorpay_key_secret))



@csrf_exempt
@require_http_methods(['POST'])
def razorpay_webhook(request):
    signature = request.headers.get('X-Razorpay-Signature')
    if not signature:
        return HttpResponse('Invalid signature', status=401)

    try:
        payload = json.loads(request.body)
        event = payload.get('event')

        if event == 'payment.succeeded':
            order_id = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.order_status = 'paid'
                    order.save()

                    user_email = order.user.email
                    subject = 'Payment Confirmation'
                    message = 'Your payment has been successfully processed.'
                    send_mail(subject, message, 'your_email@example.com', [user_email])
                except Order.DoesNotExist:
                    return HttpResponse('Order not found', status=404)

        elif event == 'payment.failed':
            order_id = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.order_status = 'failed'
                    order.save()

                    user_email = order.user.email
                    subject = 'Payment Failure'
                    message = 'Your payment has failed. Please try again.'
                    send_mail(subject, message, 'your_email@example.com', [user_email])
                except Order.DoesNotExist:
                    return HttpResponse('Order not found', status=404)

        return HttpResponse('Webhook received', status=200)
    except json.JSONDecodeError:
        return HttpResponse('Invalid payload', status=400)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)






# class CreateRazorpayOrderView(APIView):
#     def post(self, request):
#         try:
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             order_amount = request.data.get('price') * 100  
#             order_currency = 'INR'
#             order_receipt = 'order_rcptid_11'

#             order = client.order.create({
#                 'amount': order_amount,
#                 'currency': order_currency,
#                 'receipt': order_receipt,
#                 'payment_capture': '1'
#             })

#             return Response(order, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CaptureRazorpayPaymentView(APIView):
#     def post(self, request):
#         try:
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             payment_id = request.data.get('payment_id')
#             amount = request.data.get('price') * 100  

#             capture = client.payment.capture(payment_id, amount)
#             return Response(capture, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

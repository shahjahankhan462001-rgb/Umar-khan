from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail

from .models import Project, Contact
from .serializers import ProjectSerializer, ContactSerializer


@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_contact(request):

    # GET all contacts
    if request.method == "GET":
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    # POST contact + send email
    if request.method == "POST":
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            contact = serializer.save()

            name = request.data.get("name")
            email = request.data.get("email")
            subject = request.data.get("subject")
            message = request.data.get("message")

            full_message = f"""
New Message from Portfolio Website:

Name: {name}
Email: {email}

Message:
{message}
"""

            send_mail(
                subject,
                full_message,
                email,   # from email (user ka email)
                ["shahjahankhan462001@gmail.com"],  # tumhara inbox email
                fail_silently=False,
            )

            return Response(
                {
                    "message": "Message saved and email sent successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
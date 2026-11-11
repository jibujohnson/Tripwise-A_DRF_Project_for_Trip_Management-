from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer,TripSerializer
from tripmaster.models import TripDb
from rest_framework import authentication,permissions,serializers
from tripmaster.permissions import OwnerOnly

# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"User Created Successfully!"
            },status=201)
        
        return Response({
            "Message":"Invalid Data!"
        },status=400)

class UserListView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer_instance=UserSerializer(users,many=True)
        return Response(data=serializer_instance.data,status=200)

class UserDeleteView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request):
        user_object=request.user
        user_object.delete()
        return Response(data={
            "Message":"User and associated trips deleted successfully!"
        })

class TripListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        qs=TripDb.objects.filter(created_by=request.user )
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        from_data=request.data
        serializer_instance=TripSerializer(data=from_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "Message":"Trip Created Successfully!",
                "Trip Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

class TripRetrieveUpdateDeleteView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[OwnerOnly]
    
    def get(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        # 1 Trip to Paris    Paris    2026-11-11    .....
        if trip_object.created_by==request.user:
            serializer_instance=TripSerializer(trip_object)
            return Response(data=serializer_instance.data,status=200)
        else:
            return Response(data={
                "Message":"You are not allowed to access this Trip." 
            })

    def put(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        if trip_object.created_by != request.user:
            raise serializers.ValidationError("Access Denied!")
        serializer_instance=TripSerializer(trip_object,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message":"Trip details updated successfully!",
                "Updated Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        if trip_object.created_by==request.user:
            trip_object.delete()
            return Response(data={
                "Message":"Trip Deleted Successfully!" 
            })
        else:
            return Response(data={
                "Warning":"You are not allowed to delete this trip."
            },status=403)

# For Listing all users in the User [Django shell]

# users=User.objects.all()
# for user in users:
    # print(
    #     "ID:",user.id,
    #     "Username:",user.username,
    #     "Email:",user.email,
    #     "Active:",user.is_active
    # )
        

            




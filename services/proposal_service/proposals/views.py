# proposals/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Proposal
from .serializers import ProposalSerializer
import requests # ใช้สำหรับสื่อสารระหว่าง Service

class ProposalPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # ต้อง Login ก่อนเสมอ
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # เจ้าของ proposal (caregiver) สามารถดู/แก้ไข/ลบได้
        if obj.caregiver_id == request.user.id:
            return True

        # เจ้าของ JobPost สามารถดู proposal และ accept ได้
        # ในระบบจริง ต้องยิง API ไปถาม job_post_service ว่าใครคือเจ้าของ job_post_id
        # แต่เพื่อความง่าย จะสมมติว่ามีการส่ง owner_id มาด้วย
        # is_job_owner = check_job_post_owner(obj.job_post_id, request.user.id)
        # return is_job_owner
        return True # อนุญาตให้ดูก่อนเพื่อความง่ายในการทดสอบ

class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [ProposalPermission]

    def get_queryset(self):
        """
        กรอง proposal ตาม query parameter
        เช่น /proposals/?job_post_id=1 หรือ /proposals/?caregiver_id=2
        """
        queryset = Proposal.objects.all()
        job_post_id = self.request.query_params.get('job_post_id')
        caregiver_id = self.request.query_params.get('caregiver_id')

        if job_post_id:
            queryset = queryset.filter(job_post_id=job_post_id)
        if caregiver_id:
            queryset = queryset.filter(caregiver_id=caregiver_id)
            
        return queryset

    def perform_create(self, serializer):
        """
        ตอนสร้าง proposal ให้บันทึก caregiver_id เป็น id ของผู้ใช้ที่ login อยู่
        """
        serializer.save(caregiver_id=self.request.user.id)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Endpoint สำหรับเจ้าของ JobPost เพื่อ accept proposal
        """
        proposal = self.get_object()

        # --- ส่วนนี้สำคัญมากสำหรับการสื่อสารระหว่าง Service ---
        # 1. ตรวจสอบว่าคนที่กด accept เป็นเจ้าของ JobPost จริงๆ
        #    ต้องยิง API ไปถามที่ job_post_service
        #    เช่น GET /job-posts/{proposal.job_post_id}/
        #    แล้วเช็คว่า response.data['owner_id'] == request.user.id หรือไม่

        # 2. เมื่อ accept แล้ว ควรมีการส่ง Event (เช่น ผ่าน RabbitMQ, Kafka)
        #    เพื่อบอกให้ bookings_service สร้าง Booking ขึ้นมา
        #    ในตัวอย่างนี้จะแค่เปลี่ยนสถานะเท่านั้น

        if proposal.status != 'pending':
            return Response({'error': 'This proposal is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

        proposal.status = 'accepted'
        proposal.save()
        
        # (Optional) reject proposal อื่นๆ ของ job_post เดียวกัน
        Proposal.objects.filter(job_post_id=proposal.job_post_id).exclude(pk=proposal.pk).update(status='rejected')

        return Response(self.get_serializer(proposal).data)
from rest_framework import viewsets, permissions
from .models import Proposal
from .serializers import ProposalSerializer

class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Proposal.objects.filter(caregiver_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(caregiver_id=self.request.user.id)
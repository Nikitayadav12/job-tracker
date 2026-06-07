from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from applications.models import JobApplication


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        applications = JobApplication.objects.filter(user=user)

        # Count by status
        status_counts = applications.values('status').annotate(
            count=Count('id')
        ).order_by('status')

        summary = {item['status']: item['count'] for item in status_counts}

        # Fill in zeros for statuses with no applications
        all_statuses = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']
        for s in all_statuses:
            if s not in summary:
                summary[s] = 0

        return Response({
            'total': applications.count(),
            'by_status': summary,
            'this_month': applications.filter(
                applied_date__month=__import__('datetime').date.today().month,
                applied_date__year=__import__('datetime').date.today().year,
            ).count(),
        })
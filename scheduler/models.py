from django.db import models

class Schedule(models.Model):
    title = models.CharField(max_length=300)

    def as_dict(self):
        # TODO: Extract dates covered and hours from base_cluster
        return {
            'base_cluster': SlotCluster.objects.filter(schedule=self, is_base=True)[0].as_dict(),
            'user_clusters': [cluster.as_dict() for cluster in SlotCluster.objects.filter(schedule=self, is_base=False)],
        }

class SlotCluster(models.Model):
    is_base = models.BooleanField(default=False)
    owner = models.CharField(max_length=200)
    slots = models.JSONField()
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'owner': self.owner,
            'slots': self.slots,
        }

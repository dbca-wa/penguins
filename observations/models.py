from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone


class Camera(models.Model):
    """A camera represents a single recording device at one of the sites that
    penguin observations are to be recorded.
    """

    name = models.CharField(max_length=100)
    camera_key = models.CharField(
        max_length=100,
        default="",
        help_text="Space-separated list of keys to match video recordings",
    )
    location = models.PointField(srid=4326, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.active:
            return self.name
        else:
            return f"{self.name} (inactive)"

    def get_newest_video(self):
        video = Video.objects.filter(camera=self).first()  # Assumes ordering on Video.
        return video or None


class Video(models.Model):
    """A video represents a single recording from a camera on Penguin Island, against which
    penguins will be counted. Normally videos are one hour duration.
    """

    date = models.DateField(help_text="The date of the recording.")
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT)
    uploaded_file = models.FileField(upload_to="videos")
    start_time = models.TimeField(help_text="The start time of the recording.")
    end_time = models.TimeField(help_text="The end time of the recording (usually 1h after start).")
    views = models.PositiveSmallIntegerField(default=0)
    mark_complete = models.BooleanField(default=False, help_text="Has this been viewed in its entirety by a reviewer?")
    completed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="videos_seen",
        verbose_name="Users who have seen this video",
    )

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.camera.name}: {self.date} {self.start_time} - {self.end_time}"

    def get_absolute_url(self):
        return reverse("observations:video_detail", kwargs={"pk": self.pk})

    def get_video_filename(self):
        return self.uploaded_file.name.split("/")[-1]

    def get_content_disposition(self):
        filename = self.get_video_filename()
        return f"attachment; filename={filename}"

    def clean_date(self):
        if self.date > date.today():
            raise ValidationError("The 'Date' cannot be in the future!")

    def clean_end_time(self):
        if self.end_time < self.start_time:
            raise ValidationError("The 'End Time' cannot be before the 'Start Time'!")

    @property
    def duration(self):
        end = timedelta(
            hours=self.end_time.hour,
            minutes=self.end_time.minute,
            seconds=self.end_time.second,
        )
        start = timedelta(
            hours=self.start_time.hour,
            minutes=self.start_time.minute,
            seconds=self.start_time.second,
        )
        return end - start

    def get_start_datetime(self):
        return datetime.combine(self.date, self.start_time)


class PenguinObservation(models.Model):
    """Represents the observation of 0+ penguins at a particular frame within a video.
    More than one observation of the same penguins on the same video may exist, if >1 person
    watches the video and records an observation.
    """

    video = models.ForeignKey(Video, on_delete=models.PROTECT)
    observer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="observations", on_delete=models.PROTECT)
    position = models.FloatField(
        default=0,
        null=True,
        verbose_name="Position (s)",
        help_text="Position in video (seconds from start)",
    )
    count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="The count of penguins counted in this observation.",
    )
    comments = models.TextField(blank=True, null=True)
    raining = models.BooleanField(default=False, help_text="Was it raining at the time of the observation?")
    validated = models.BooleanField(default=True, verbose_name="Confirmed")

    def __str__(self):
        return "{} penguin(s) counted on {} at {} by {}".format(
            self.count,
            self.video.camera.name,
            self.get_observation_datetime(),
            self.observer,
        )

    def get_observation_datetime(self):
        """From the associated video and the value of `position`, derive the datetime of the penguin observation."""
        start = datetime.combine(self.video.date, self.video.start_time).astimezone(timezone.get_current_timezone())
        return start + timedelta(seconds=self.position)

from django.db import models
from django.conf import settings

class Person(models.Model):
    class Meta:
        unique_together = ('first_name', 'last_name')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.name


class Link(models.Model):
    """ Link for person's external accounts """
    url = models.CharField(max_length=100)
    person = models.ForeignKey(Person, blank=True, null=True)


class Organization(models.Model):
    """ External affiliations for users """
    url = models.CharField(max_length=100)
    persons = models.ManyToManyField(Person, blank=True, null=True, related_name="organisations")


class Project(models.Model):
    """ Project in community """
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    logo = models.ImageField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)

    def __unicode__(self):
        return self.name


class Edition(models.Model):
    """ Project edition """
    project = models.ForeignKey(Project, related_name="editions")
    picture = models.ImageField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)
    name = models.CharField(max_length=100)

    # TODO: add date interval
    persons = models.ManyToManyField(Person, through='PersonRole')

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """ A role that can be given to many persons in an edition """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class PersonRole(models.Model):
    person = models.ForeignKey(Person, related_name="person_roles")
    edition = models.ForeignKey(Edition, related_name="person_roles")
    role = models.ForeignKey(Role)

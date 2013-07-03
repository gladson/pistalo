# coding: utf-8
from django.db import models
from PIL import Image


class GaleriaQuerySet(models.query.QuerySet):
    def ativos(self):
        return self.filter(ativo=True)


class GaleriaManager(models.Manager):
    def get_query_set(self):
        return GaleriaQuerySet(self.model, using=self._db)

    def ativos(self):
        return self.get_query_set().ativos()


class Galeria(models.Model):
    ordenacao = models.PositiveSmallIntegerField(u'Ordenação', default=0)
    nome = models.CharField(max_length=120)
    desc = models.TextField(u'Descrição', blank=True)
    thumb = models.ImageField(upload_to='galeria')
    imagem = models.ImageField(upload_to='galeria')
    ativo = models.BooleanField(default=False)

    data_criacao = models.DateTimeField(
        verbose_name=u'Data de criação',
        auto_now_add=True,
        editable=True
    )
    data_atualizacao = models.DateTimeField(
        verbose_name=u'Data de atualização',
        auto_now=True,
        editable=True
    )

    objects = GaleriaManager()

    def save(self, *args, **kwargs):
        # Save this one
        super(Galeria, self).save(*args,**kwargs)

        # resize on file system
        size = 160, 160
        filename = str(self.thumb.path)
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    class Meta:
        ordering = ['ordenacao', 'nome']

    def __unicode__(self):
        return self.nome

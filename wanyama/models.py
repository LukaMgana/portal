from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.urls import reverse, reverse_lazy

import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from .choices import *


class Category(models.Model):
    category_id             = models.AutoField(_("Category"), primary_key = True)
    title                   = models.CharField(_("Category Title"), choices=CATEGORY, max_length=150)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    

class Livestock(models.Model):
    livestock_id            = models.AutoField(_("Livestock id"), primary_key=True)
    livestock_name          = models.CharField(_('Livestock name'), max_length = 244)
    gender                  = models.CharField(_("Animal Gender"),choices = GENDER, max_length = 255)
    status                  = models.CharField(choices = CATTLE_STATUS, max_length = 255)
    birth_date              = models.DateField(_("Birth Date"),)
    location                = models.CharField(max_length=244, null= True)
    weight                  = models.PositiveIntegerField(null=True)
    ls_image                = models.ImageField(_("Cattle Images"), null = True, upload_to = 'media', blank=True)
    cartegory               = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    owner                   = models.ForeignKey('farmer.Farmer', blank=True, null = True, on_delete = models.CASCADE)
    color                   = models.CharField(max_length=244, blank=True, null = True)
    horns                   = models.CharField(max_length=244, blank=True, null = True)
    breed                   = models.CharField(max_length=244, blank=True, null = True)

    def __str__(self):
        return self.livestock_name
    
    def get_absolute_url(self):
        return reverse("wanyama:index")
    



class Tag(models.Model):
    tag_id   = models.AutoField(_('Tag id'), primary_key= True)
    tag                     = models.ImageField(_("Image Tag"), blank=True,  null=True, upload_to = 'media/tags')
    tag_type                = models.CharField(_("Tag Type"),max_length = 255, default = 'QR-code')
    livestock               = models.OneToOneField(Livestock, null= True, on_delete= models.CASCADE)

    def __str__(self):
        return "Animal Tag: " + self.tag_type
    
    
    def save(self, *args, **kwargs):
        data =f'\n\
                Owner: {str(self.livestock.owner)}\n\
                Name: {str(self.livestock.owner)}\n\
                Gender: {str(self.livestock.gender)}\n\
                Status: {str(self.livestock.status)}\n\
                Category: {str(self.livestock.cartegory)}\n\
                Color: {str(self.livestock.color)}\n\
                Location: {str(self.livestock.location)}\n\
                Weight: {str(self.livestock.weight)} kg(s)\n\
                    '

        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=1,
            # error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8, 
            border=2,             
            image_factory=None,
            mask_pattern=None
        )
        qr.add_data(data)
        qr.make(fit=True)

        tag_img = qr.make_image(fill_color='black', back_color='white', size = 5, scale=5)
       
        canvas = Image.new('RGB', (550, 550), 'white')
        ImageDraw.Draw(canvas)
        canvas.paste(tag_img)
        fname = f'qr_code-{str(self.livestock)}.PNG'


        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.tag.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)



class Livestock_Health(models.Model):
    livestok_heath_id        = models.AutoField(primary_key=True)
    disability              = models.CharField(_("Has Disability?"), max_length=255, choices = BOOLCHOICE)
    medication              = models.CharField(_("Takes Drugs?"), max_length=255, choices = BOOLCHOICE)
    descriptions            = models.CharField(_("Explanations"), max_length=255, blank=True, null=True)
    health                  = models.OneToOneField(Livestock, verbose_name=_("Health Status"), blank = True, null = True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Health'
    
    def __str__(self):
        return str(self.health) + ": has disability " + str(self.disability)  + ", takes drugs " + str(self.medication)
    


class ExpenseIncome(models.Model):
    ei_id = models.AutoField(_('Id'), primary_key=True)
    farmer                  = models.ForeignKey('farmer.Farmer', on_delete=models.CASCADE, blank=True, null=True)
    amount                  = models.DecimalField(_("Amount"), max_digits=20, decimal_places=2)
    descriptions            = models.TextField(_("Due to "), max_length=255)
    ei_type                 = models.CharField(_("Source"), choices=IE_CHOICE, max_length=250)
    due_date                = models.DateField(_('Due date'),)

    def __str__(self):
        return str(self.amount) + " due to " + self.ei_type + " on " +str(self.due_date)

    class Meta:
        verbose_name_plural = 'Expenses and Incomes'
    


class Report(models.Model):
    report_id = models.AutoField(_('Report id'), primary_key=True)
    printed_report          = models.FileField(_("Erliar Printed"), upload_to='media/printedRiports', max_length=100)


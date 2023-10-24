from django.contrib import admin
from .models import Video,DownloadItem, Video_Ea,Faq,Payment
from .forms import VideoForm
from django import forms
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ('title', 'description')  # Customize this list as needed

admin.site.register(Video, VideoAdmin)


class DownloadForm(forms.ModelForm):
    class Meta:
        model = DownloadItem
        fields = ['title', 'file']
admin.site.register(DownloadItem)

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video_Ea
        fields = ['title', 'youtube_url']
admin.site.register(Video_Ea)


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
admin.site.register(Faq)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'amount', 'payment_date']
    list_filter = ['payment_date']
    search_fields = ['user__username', 'transaction_id']
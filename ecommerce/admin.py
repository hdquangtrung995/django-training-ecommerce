from django.contrib import admin
from ecommerce.models import (
    EcomCategory,
    EcomProducts,
    EcomProductVariant,
    EcomPromotion,
    EcomCustomerOrder,
    EcomPayment,
    EcomProductReview,
    EcomStore,
    EcomStoreBranch,
    EcomStoreGuideline,
)

# Register your models here.
admin.site.register(EcomCategory)
admin.site.register(EcomProducts)
admin.site.register(EcomProductVariant)
admin.site.register(EcomPromotion)
admin.site.register(EcomCustomerOrder)
admin.site.register(EcomPayment)
admin.site.register(EcomProductReview)
admin.site.register(EcomStore)
admin.site.register(EcomStoreBranch)
admin.site.register(EcomStoreGuideline)

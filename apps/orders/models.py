# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
# from uuid import uuid4

# from apps.base_models.models import BaseModel
# # Create your models here.


# class Orders(BaseModel):
#     created = None
#     modified = None
#     STATUS = (
#         ('ordered', _('Ordered')),
#         ('paid', _('Paid')),
#         ('delivered', _('Delivered')),
# )

#     id      = models.UUIDField(_("ID"), default=uuid4, editable=False, primary_key=True, unique=True)
#     name    = models.CharField(_("Client name"), max_length=128)
#     address = models.CharField(_("Order address")max_length=3000, blank=True)
#     phone   = PhoneNumberField()
#     status  = models.CharField(choices=STATUS, max_length=20)

#     class Meta:
#         ordering = ("-created_at", "-modified_at")
#         verbose_name = _("Order")
#         verbose_name_plural = _("Orders")

#     def __str__(self):
#         return '%i-%s'%(
#             self.id, self.name)

#     @property
#     def products(self):
#         return self.orderitems.all()


# class OrderItems(BaseModel):
#     created = None
#     modified = None

#     id       = models.UUIDField(_("ID"), default=uuid4, editable=False, primary_key=True, unique=True)
#     order    = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
#     product  = models.ForeignKey("apps.products.Products", on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField(_("Product Quantity"))
#     message  = models.CharField(_("Client Message"), null=True, blank=True)

#     class Meta:
#         db_table = "orders_order_item"
#         ordering = ("-created_at", "-modified_at")
#         verbose_name = _("Order Item")
#         verbose_name_plural = _("Order Items")

#     def __str__(self):
#         return '%i-%s'%(
#             self.id, self.order.name if self.order and hasattr(self.order, 'name') else None)
     
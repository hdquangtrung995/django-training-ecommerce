from ecommerce.models import EcomProducts, EcomProductVariant


class ProductsController:
    def get_all_products():
        return EcomProducts.objects.filter(is_active=True)

    def get_one_product(self, *, id, slug):
        if id:
            return EcomProducts.objects.get(pk=id)
        elif slug:
            return EcomProducts.objects.get(slug=slug)
        else:
            raise "Not found"

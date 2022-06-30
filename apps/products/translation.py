from modeltranslation.translator import TranslationOptions, translator


from . import models


class CategoriesTranslation(TranslationOptions):
    fields = ('title', )

translator.register(models.Categories, CategoriesTranslation)

class SubCategoriesTranslation(TranslationOptions):
    fields = ('title', )

translator.register(models.SubCategories, SubCategoriesTranslation)

class ProductsTranslation(TranslationOptions):
    fields = ('title', 'description', 'characteristics', )

translator.register(models.Products, ProductsTranslation)

class PromotionsTranslation(TranslationOptions):
    fields = ('title', 'description', )

translator.register(models.Promotions, PromotionsTranslation)



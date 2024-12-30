class CalculatePromotionDiscount {
    constructor(promotions=[]) {
        this.promotions = promotions
        this.promotionType = {
            product: 0,
            coupon: 1,
            flashsale: 2,
            freeship: 3
        }
        this.discountType = {
            percentage: 0,
            fixed: 1
        }
    }

    isNumeric(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }

    calculateDiscountValueBaseOnDiscountType(promotion, basePrice) {
        const discountVariant = promotion.discount_variant
        const maxDiscount = parseFloat(discountVariant.max_discount)
        const discountValue = parseFloat(discountVariant.discount_value)
        if (!this.isNumeric(basePrice) && !this.isNumeric(maxDiscount) && !this.isNumeric(discountValue)) throw 'Not a valid number!'

        if (discountVariant.discount_type.value ===  this.discountType.percentage) {
            let result = basePrice * discountValue / 100
            result = maxDiscount && result > maxDiscount ? maxDiscount : result 
            return result
        } else {
            let result = discountValue
            result = maxDiscount && result > maxDiscount ? maxDiscount : result 
            return result
        }
    }
    
    productLevelPromotionDiscountValue(selectedVariant) {
        const price = {
            basePrice: 0,
            discountedPrice: 0
        }
        try {
            
            const basePrice = parseFloat(selectedVariant.price)
            const quantity = selectedVariant.quantity
            price.basePrice = basePrice

            if (!this.promotions.length) return price
            

            const flashSale = this.promotions.find(item => item.promotion_type.type === this.promotionType.flashsale)
            if (flashSale) {
                const discount =  this.calculateDiscountValueBaseOnDiscountType(flashSale, price.basePrice)
                price.discountedPrice = price.basePrice - discount
                return price
            }

            const productSale = this.promotions.find(item => item.promotion_type.type === this.promotionType.product)
            if (productSale) {
                const discount = this.calculateDiscountValueBaseOnDiscountType(productSale, price.basePrice)
                price.discountedPrice = price.basePrice - discount
                return price
            }
            return price
        } catch (error) {
            console.error(error);
            return price
        }
    }
}

export default CalculatePromotionDiscount

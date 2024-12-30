import DeliveryFee from './delivery-fee.js'

class OrderDetail {
    #csrf_token;

    constructor(csrf_token, cartUrl, cartInstance, PromotionCoupon, CalculatePromotionDiscount) {
        this.#csrf_token = csrf_token
        this.cartUrl = cartUrl
        this.cartInstance = cartInstance

        this.products = []
        this.promotions = []
        this.orderNoteValue = ''
        this.promotionCodeValue = ''

        this.estimate = 0
        this.discounted = 0
        this.deliveryFee = 0
        this.discountedDeliveryFee = 0
        this.totalPriceToPay = 0
        this.discountedTotalToPay = 0

        this.deliveryObject = new DeliveryFee(this.#csrf_token, this.resetDelivery.bind(this))
        this.promotionsCouponObject = new PromotionCoupon()
        this.calculatePromotionDiscountObject = new CalculatePromotionDiscount()
        
        this.estimatePriceId = 'estimate-price'
        this.discountedPriceId = 'discounted-price'
        this.deliveryFeeId = 'delivery-price'
        this.deliveryPriceToPayId = 'delivery-price-to-pay'
        this.totalPriceId = 'totel-price'
        this.totalPriceToPayId = 'total-price-to-pay'
        
        this.orderNoteId = 'order-note'
        this.promotionCodeId = 'promotion-code'
        
        this.buttonApplyPromotionId = 'button-apply-promotion'
        
        const first_layer = JSON.parse($('#promotions-list').text())
        if (first_layer) {
            this.promotions =   JSON.parse(first_layer)
            $('#promotions-list').remove();
        }
    }

    render(data) {
        this.products = data
        this.products.forEach(item => item.render())

        this.promotionsCouponObject.renderFreeship(this.promotions, this.deliveryFee)
        this.getValidPromotionCoupon()

        this.calculateOverallPrice()

        this.deliveryObject.registerProvinceOption()
        this.deliveryObject.registerDeliveryFeeClickEvent(function onGetFeeSuccess(fee) {
            this.deliveryFee = fee
            this.calculateOverallPrice()
            this.validateDeliveryPromotion()
            $(`#${this.deliveryFeeId}`).removeClass('line-through')
        }.bind(this))
        this.registerApplyPromotionClickEvent()
    }

    calculateOverallPrice() {
        this.handleUpdateEstimatePrice()
        this.handleUpdateDiscountedPrice()
        this.handleUpdateDeliveryFee()
        this.handleUpdateTotalPrice()
    }

    handleUpdateEstimatePrice() {
        const estimate = this.products.reduce((acc, curr) => (parseFloat(curr.selectedVariant.price) * curr.selectedVariant.quantity) + acc, 0)
        this.estimate = estimate
        $(`#${this.estimatePriceId}`).text(convertDecimalToHumanReadable(this.estimate))
    }

    handleUpdateDeliveryFee() {
        $(`#${this.deliveryFeeId}`).text(convertDecimalToHumanReadable(this.deliveryFee))
    }

    handleUpdateDiscountedPrice() {
        const discounted = this.products.reduce((acc, curr) => (parseFloat(curr.discountedPurchasePrice) * curr.selectedVariant.quantity) + acc, 0)
        this.discounted = discounted
        $(`#${this.discountedPriceId}`).text(convertDecimalToHumanReadable(this.discounted))
    }

    handleUpdateTotalPrice() {
        // The order of these operation matters
        // Proceed with caution when updating
        const deliveryToPay = this.deliveryFee - this.discountedDeliveryFee
        this.totalPriceToPay = this.estimate - this.discounted + deliveryToPay
        const totalPriceToPay = this.totalPriceToPay - this.discountedTotalToPay

        $(`#${this.totalPriceId}`).text(convertDecimalToHumanReadable(this.totalPriceToPay))
        
        if (this.discountedDeliveryFee) {
            $(`#${this.deliveryFeeId}`).addClass('line-through')
            $(`#${this.deliveryPriceToPayId}`).text(convertDecimalToHumanReadable(deliveryToPay)).show()
        }

        if (this.discountedTotalToPay) {
            $(`#${this.totalPriceId}`).addClass('line-through')
            $(`#${this.totalPriceToPayId}`).text(convertDecimalToHumanReadable(totalPriceToPay)).show()
        }
    }

    handleProductUpdate(product) {
        const availableProducts = this.products.filter(i => i.selectedVariant.id === product.selectedVariant.id)
        if (availableProducts.length < 2) {
            const id = availableProducts[0].selectedVariant.id
            const itemIndex = this.products.findIndex(i => i.selectedVariant.id === id)
            if (itemIndex !== -1) {
                this.products[itemIndex] = availableProducts[0]
                this.calculateOverallPrice()
            }
        } else {
            const productUniqueId = product.uniqueIdentifier
            const itemIndex = this.products.findIndex(i => i.uniqueIdentifier === productUniqueId);
            if (itemIndex !== -1) {
                $(`#${productUniqueId}`).remove()
                this.products.splice(itemIndex, 1)
                this.products.forEach(item => item.render())
                this.calculateOverallPrice()
            }
        }
        this.getValidPromotionCoupon()
    }

    handleProductRemove(product) {
        const productUniqueId = product.uniqueIdentifier
        const itemIndex = this.products.findIndex(i => i.uniqueIdentifier === productUniqueId);
        if (itemIndex !== -1) {
            this.products.splice(itemIndex, 1)
            this.calculateOverallPrice()
            this.getValidPromotionCoupon()
        }
    }

    getValidPromotionCoupon() {
        const self = this;
        $.ajax({
            url: self.cartUrl,
            method: "GET",
            contentType: "application/json",
            data: { contextonly: JSON.stringify(self.cartInstance.cartItems) },
            headers: {
                "X-CSRFToken": `${self.#csrf_token}`
            },
            beforeSend: function() {},
            success: function(response) {
                self.promotionsCouponObject.renderCoupon(response)
            },
            error: function(xhr, status, error) {
                console.error("Submission failed:", status, error);
            }
        })
    }

    resetDelivery() {
        this.resetOrderDetailPricingAndDOMDisplay()
        this.promotionsCouponObject.setDeliveryPromotionDisableAttrs(true)
        this.calculateOverallPrice()
    }

    validateDeliveryPromotion() {
        // Check if total order is satisfy delivery coupon condition
        // If satisfied, enable delivery coupon
        const deliveryPromotions = this.promotions.filter(item => item.promotion_type.type === 3)
        deliveryPromotions.forEach(item => {
            const discountVariant = item.discount_variant
            const totalQuantity = this.products.reduce((acc, curr) => curr.selectedVariant.quantity + acc, 0)
            const inputElement = $(`#${item.code}`)

            const isQuantitysatisfied = (() => {
                const { min_item, max_item } = discountVariant;
                if (min_item >= 0 && max_item === 0) {
                    return totalQuantity >= min_item
                } else if (min_item !== 0 && max_item !== 0) {
                    return totalQuantity >= min_item && totalQuantity <= max_item
                }
                return true
            })()

            const isTotalPriceSatisfied = (() => {
                const { min_purchase, max_purchase } = discountVariant;
                const min = parseFloat(min_purchase)
                const max = parseFloat(max_purchase)
                if (min >= 0 && max === 0) {
                    return this.totalPriceToPay >= min
                } else if (min !== 0 && max !== 0) {
                    returntotalPriceToPay >= min && this.totalPriceToPay <= max
                }
                return true
            })()
            if (isQuantitysatisfied && isTotalPriceSatisfied) {
                inputElement.prop('disabled', false)
            }
        })
    }

    registerApplyPromotionClickEvent() {
        $(`#${this.buttonApplyPromotionId}`).on('click', function() {
            const deliveryRadioElement = $(`input[name="${this.promotionsCouponObject.freeshipRadioName}"]:checked`)
            const couponRadioElement = $(`input[name="${this.promotionsCouponObject.couponRadioName}"]:checked`)

            if (deliveryRadioElement.length) {
                const code = deliveryRadioElement.val()
                const promotion = this.promotions.find(item => item.code === code)
                if (promotion) {
                    const discount = this.calculatePromotionDiscountObject.calculateDiscountValueBaseOnDiscountType(promotion, this.deliveryFee)
                    this.discountedDeliveryFee = discount
                }
            }

            if (couponRadioElement.length) {
                const code = couponRadioElement.val()
                const promotion = this.promotions.find(item => item.code === code)
                if (promotion) {
                    const discount = this.calculatePromotionDiscountObject.calculateDiscountValueBaseOnDiscountType(promotion, this.totalPriceToPay)
                    this.discountedTotalToPay = discount
                }
            }

            if (deliveryRadioElement.length || couponRadioElement.length) this.handleUpdateTotalPrice()
        }.bind(this))
    }

    resetOrderDetailPricingAndDOMDisplay() {
        this.deliveryFee = 0
        this.discountedDeliveryFee = 0
        this.discountedTotalToPay = 0
        $(`#${this.deliveryPriceToPayId}`).hide()
        $(`#${this.deliveryFeeId}`).removeClass('line-through')

        $(`#${this.totalPriceId}`).removeClass('line-through')
        $(`#${this.totalPriceToPayId}`).hide()
    }
}

export default OrderDetail

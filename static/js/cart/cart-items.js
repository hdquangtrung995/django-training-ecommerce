class CartItem {
    constructor(CalculatePromotionDiscount, product, productUrl='', cartInstance = {}, updateItemCb, removeItemCb) {
        this.product = product
        this.selectedVariant = product.selectedVariant
        this.variants = product.variants
        this.cartInstance = cartInstance
        this.updateItemCb = updateItemCb
        this.removeItemCb = removeItemCb
        this.calculatePromotionDiscount = new CalculatePromotionDiscount(this.product.promotions)

        this.finalPurchasePrice = 0
        this.discountedPurchasePrice = 0
        this.priceTop = 0
        this.priceBottom = 0

        this.productUrl = productUrl.split('/replaceMe')[0]
        this.containerId = 'cart-element-container'
        this.uniqueIdentifier = Math.random().toString(36).substr(2, 9);
        this.selectInputContainerId = 'select-container'.concat('-', this.uniqueIdentifier)
        this.decrementId = 'decrement'.concat('-', this.uniqueIdentifier)
        this.incrementId = 'increment'.concat('-', this.uniqueIdentifier)
        this.quantityId = 'quantity'.concat('-', this.uniqueIdentifier)
        this.removeCartItemId = 'remove-cart'.concat('-', this.uniqueIdentifier)
        this.originalCartItemPriceId = 'original-cart-item-price'
        this.discountedCartItemPriceId = 'discounted-cart-item-price'
    }

    sizeOptionString(id, label, value) {
        return `<option data-variant="${id}" value="${value}" ${this.selectedVariant.size.value == value ? 'selected' : ''}>${label}</option>`
    }

    sizeSelectOptionString() {
        const groupingSize = this.variants.filter(i => this.selectedVariant.color && i.color == this.selectedVariant.color).reduce((acc, curr) => {
            return { ...acc, [curr.size.value]: {...curr.size, id: curr.id} }
        }, {})

        const outputString = Object.values(groupingSize).reduce((acc, curr) => acc + this.sizeOptionString(curr.id, curr.label, curr.value), '')
        return `<select id="${this.selectInputContainerId}" name="options">${outputString}</select>`
    }

    cartItemElementString() {
        return `
            <div id="${this.uniqueIdentifier}" class="w-full pb-4 border-b flexRow">
                <div class="w-1/5"><a class="" href="${this.productUrl.concat('/', this.product.slug)}"><img src="${this.product.thumbnail}"></a></div>

                <div class="w-4/5 pl-2 flexCol justify-between relative">
                    <span class="max-w-[90%] line-clamp-2 text-ellipsis overflow-hidden"><a href="${this.productUrl.concat('/', this.product.slug)}" class="self-start hover:text-[#FB8500]">${this.product.name}</a></span>
                    
                    <div class="">
                        <div class="flexRow gap-2 items-center">
                            <span class="capitalize">${this.selectedVariant.color ? `${this.selectedVariant.color}-`: ''}${this.selectedVariant.sku}</span>
                            ${this.selectedVariant.color || this.selectedVariant.size ? '<span> / </span>'.concat(this.sizeSelectOptionString()) : ''}
                        </div>
                    </div>
                    <div class="flexRowBetween">
                        <div class="">
                            <div class="flexRowCenter self-start md:self-auto h-10 border has-[:disabled]:bg-gray-200">
                                <button id="${this.decrementId}" class="w-10 text-lg font-bold disabled:cursor-not-allowed" disabled>-</button>
                                <input type="number" id="${this.quantityId}" name="quantity" min="1" max="${this.selectedVariant.stock}" value="${this.selectedVariant.quantity}" class="w-10 text-lg font-bold text-center bg-white hideInputNumberArrow disabled:cursor-not-allowed disabled:bg-gray-200" disabled>
                                <button id="${this.incrementId}" class="w-10 text-lg font-bold disabled:cursor-not-allowed" disabled>+</button>
                            </div>
                        </div>
                        <div class="flexCol">
                            <span id="${this.discountedCartItemPriceId}" class="font-bold line-through text-right">
                                ${convertDecimalToHumanReadable(this.priceTop)}
                            </span>
                            <span id="${this.originalCartItemPriceId}" class="font-bold  text-right">
                                ${convertDecimalToHumanReadable(this.priceBottom)}
                            </span>
                        </div>
                    </div>
                    
                    <button id="${this.removeCartItemId}" class="absolute top-0 right-0"><i class="fa fa-remove" style="font-size: 20px;"></i></button>
                </div>
            </div>
        `
    }

    #getProductIdentifier() {
        return [this.product.id, this.selectedVariant.color, this.selectedVariant.size?.value].filter(Boolean).join('.')
    }

    handleSizeChange(self) {
        const variantId = $(this).find(':selected').attr('data-variant')
        const variant = self.variants.find(i => variantId && i.id === +variantId)

        if (variantId && variant) {
            const currentLocalStoreCartId = [self.product.id, self.selectedVariant.color, self.selectedVariant.size?.value].filter(Boolean).join('.')
            self.cartInstance.removeCartItem(currentLocalStoreCartId)

            self.selectedVariant = {...variant, quantity: 1}

            const newLocalStoreCartId = self.#getProductIdentifier()
            self.cartInstance.addToCart(newLocalStoreCartId, self.selectedVariant.color, self.selectedVariant.size?.value, self.selectedVariant.quantity, self.selectedVariant.id)
            self.render()
            self.updateItemCb?.(self)
        }
    }

    handleRemoveCartItem(self) {
        $(`#${this.removeCartItemId}`).on('click', function() {
            self.cartInstance.removeCartItem(self.#getProductIdentifier())
            $(`#${self.uniqueIdentifier}`).remove()
            self.removeItemCb?.(self)
        })
    }

    registerQuantityChange(self) {
        $(`#${this.incrementId}`).on('click', function() {
            if (self.selectedVariant.quantity < self.selectedVariant.stock) {
                self.selectedVariant.quantity += 1
                self.cartInstance.updateItemQuantity(self.#getProductIdentifier(),  self.selectedVariant.quantity)
                $(`#${self.quantityId}`).val(self.selectedVariant.quantity)
                self.updateItemCb?.(self)
            };
        });

        $(`#${this.decrementId}`).on('click', function() {
            const minValue = parseInt($(`#${self.quantityId}`).attr('min'));
            if (self.selectedVariant.quantity > minValue) {
                self.selectedVariant.quantity -= 1
                self.cartInstance.updateItemQuantity(self.#getProductIdentifier(),  self.selectedVariant.quantity)
                $(`#${self.quantityId}`).val(self.selectedVariant.quantity)
                self.updateItemCb?.(self)
            };
        });

        $(`#${this.quantityId}`).on('input', function() {
            const currentValue = parseInt($(this).val()) ? parseInt($(this).val()) : 0;
            if (currentValue > self.selectedVariant.stock) {
                self.selectedVariant.quantity = self.selectedVariant.stock
                $(this).val(self.selectedVariant.stock);
                self.updateItemCb?.(self)
            } else {
                self.selectedVariant.quantity = currentValue
                $(this).val(self.selectedVariant.quantity);
                self.updateItemCb?.(self)
            }
            self.cartInstance.updateItemQuantity(self.#getProductIdentifier(),  self.selectedVariant.quantity)
        });

        if (this.selectedVariant.stock > 0) {
            $(`#${this.incrementId}, #${this.decrementId}, #${this.quantityId}`).prop('disabled', false)
        }
    }

    registerSelectOption(self) {
        $(`#${this.selectInputContainerId}`).on('change', function() {
            self.handleSizeChange.call(this, self)
        })
    }

    registerFunctionality() {
        const self = this;
        this.registerSelectOption(self)
        this.registerQuantityChange(self)
        this.handleRemoveCartItem(self)
    }

    render() {
        const existing = $(`#${this.containerId}`).find(`#${this.uniqueIdentifier}`)
        const { basePrice, discountedPrice } = this.calculatePromotionDiscount.productLevelPromotionDiscountValue(this.selectedVariant)
        this.discountedPurchasePrice = discountedPrice ? basePrice - discountedPrice : 0
        this.finalPurchasePrice = discountedPrice ? discountedPrice : basePrice
        this.priceTop = discountedPrice ? basePrice : 0
        this.priceBottom = this.finalPurchasePrice

        if (existing.length) {
            existing.replaceWith($(this.cartItemElementString()))
        } else {
            $(`#${this.containerId}`).append($(this.cartItemElementString()))
        }
        this.registerFunctionality()
    }
}

export default CartItem

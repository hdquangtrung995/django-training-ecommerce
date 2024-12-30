class Cart {
    localStorageKey = 'cart'

    constructor() {
        if (Cart.instance) {
            return Cart.instance
        }

        this.itemCount = 0
        this.cartItems = {}

        if (window.localStorage.getItem(this.localStorageKey)) {
            const existingCart = JSON.parse(window.localStorage.getItem(this.localStorageKey))
            this.cartItems = existingCart
            this.updateCartCounter()
        }

        Cart.instance = this
    }

    addToCart(id, color=null, size=null, quantity=0, variantId=null) {
        // id = [<product_id>, <variant_color>, <variant_size_value>]
        // In case color and size are not available, use product id only
        const data = { [id]: { quantity, color, size, variantId } }
        this.cartItems = {...this.cartItems, ...data}
        this.updateCartCounter()
        this.updateToLocalStore()
    }

    updateToLocalStore() {
        window.localStorage.setItem(this.localStorageKey, JSON.stringify(this.cartItems))
    }

    updateCartCounter() {
        const element = document.querySelector('[data-cart-counter]')
        this.itemCount = Object.keys(this.cartItems).length
        if (element) {
            if (this.itemCount) {
                element.setAttribute('data-cart-counter', this.itemCount)
                element.classList.add('cartCounter');
            } else {
                element.setAttribute('data-cart-counter', 0)
                element.classList.remove('cartCounter');
            }
        }
    }

    isProductExistInLocalStore(id) {
        return Object.entries(this.cartItems).find(([key, _]) => id === key)
    }

    removeCartItem(id) {
        try {
            if (this.isProductExistInLocalStore(id)) {
                Reflect.deleteProperty(this.cartItems, id)
                this.updateCartCounter()
                this.updateToLocalStore()
                return true
            } else {
                throw 'Item not found in localstorage!'
            }
        } catch (error) {
            console.warn(error)
            return False
        }
    }

    updateItemQuantity(id, quantity) {
        try {
            if (this.isProductExistInLocalStore(id)) {
                this.cartItems = {...this.cartItems, [id]: { ...this.cartItems[id], quantity }}
                this.updateToLocalStore()
                return true
            } else {
                throw 'Item not found to update in localstorage!'
            }
        } catch (error) {
            console.warn(error)
            return False
        }
    }
}

$(document).ready(function() {
    $('.product-details-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: true,
        asNavFor: '.product-details-slider-nav',
        prevArrow: $('#slickProductDetailPrev'),
        nextArrow: $('#slickProductDetailNext')
    });
    $('.product-details-slider-nav').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: '.product-details-slider',
        dots: true,
        centerMode: true,
        focusOnSelect: true,
        arrows: false,
        appendDots: $(".productDetailDots"),
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2
                }
            },
        ]
    });
})

$(document).ready(function() {
    const productDetail = JSON.parse($('#product_detail').text())
    const variants = productDetail.variants.map(({color, color_hex, gender, id, price, product, size, sku, stock}) => ({ color, colorHex: color_hex, gender, id, price, product, size, sku, stock }))
    $('#product_detail').remove();

    let maxValue = 1;
    let quantityValue = 0;
    let variantId = null;

    const grouping_variant = variants.reduce((acc, curr) => {
        const { id } = curr
        return {...acc, [id]: curr}
    }, {})
    const grouping_color_test = Object.entries(grouping_variant).reduce((acc, curr) => {
        const [_, variant] = curr
        if (variant.color) {
            if (acc[variant.color]) {
                const data = [...acc[variant.color].variants, variant]
                return {...acc, [variant.color]: { variants: data.sort(({size: sizeA}, {size: sizeB}) => sizeA.value - sizeB.value), stockNotAvailable: data.every(i => i.stock <= 0) }}
            } else {
                return {...acc, [variant.color]: { variants: [variant], stockNotAvailable: variant.stock <= 0 }}
            }
        } else {
            return acc
        }
    }, {})
    const grouping_sizes_test = Object.entries(grouping_variant).reduce((acc, curr) => {
        const [_, variant] = curr
        if (variant.size) {
            return {...acc, [variant.size.value]: { value: variant.size.value, label: variant.size.label }}
        } else {
            return acc
        }
    }, {})
    const isColorAvailable = Boolean(Object.keys(grouping_color_test).length)
    const isSizeAvailable = Boolean(Object.keys(grouping_sizes_test).length)

    const sorted_color_test = Object.entries(grouping_color_test).sort(([a], [b]) => a.localeCompare(b, 'en', { sensitivity: 'base' }));
    const sorted_size_test = Object.values(grouping_sizes_test).sort((a, b) => a.value - b.value)

    function insertRadioColors() {
        const elements = sorted_color_test.map(([i, _]) => `
            <div class="relative w-7 h-7 rounded-full border border-black has-[:checked]:border-[#FB8500]">
                <input id="${i}" type="radio" name="color-radio-name" value="${i}" class="color-radio-input appearance-none peer">
                <div class="hidden peer-disabled:block cursor-not-allowed absolute z-20 top-0 left-0 w-full h-full"><div class="ban-icon"></div></div>
                <label for="${i}" class="cursor-pointer absolute w-full h-full top-0 left-0 rounded-full flexRowCenter"><div class="rounded-full w-4 h-4" style="background-color: ${i}"></div></label>
            </div>
        `)
        $('#color-wrapper').html(elements.join(''))
    }
    insertRadioColors()
    
    function insertRadioSizes() {
        const elements = sorted_size_test.map(i => `
            <div class="relative w-10 h-10 has-[:checked]:border-[#FB8500]">
                <input id="${i.value}" type="radio" name="size-radio-name" value="${i.value}" class="size-radio-input appearance-none peer">
                <div class="hidden peer-disabled:block cursor-not-allowed absolute z-20 top-0 left-0 w-full h-full"><div class="ban-icon-without-circle"></div></div>
                <label for="${i.value}" class="peer-checked:border-[#FB8500] peer-checked:*:*:block cursor-pointer absolute top-0 left-0 w-full h-full border rounded-md">
                    <div class="uppercase w-10 h-10 relative flexRowCenter">
                        <span>${i.label}</span>
                        <img class="peer-checked:block absolute hidden right-px bottom-px" src="https://file.hstatic.net/200000525917/file/select-pro_e3e51c75e13340c1805618324bab59f0.png" width="12" height="12" >
                    </div>
                </label>
            </div>
        `)
        $('#size-wrapper').html(elements.join(''))
    }

    insertRadioSizes()

    function handleQuantityInput(maxValue) {

        $('#increment').on('click', function(event) {
            event.preventDefault()
            if (quantityValue < maxValue) {
                quantityValue = quantityValue + 1
                $('#quantity').val(quantityValue)
            };
        });
    
        $('#decrement').on('click', function(event) {
            event.preventDefault()
            const minValue = parseInt($('#quantity').attr('min'));
            if (quantityValue > minValue) {
                quantityValue = quantityValue - 1
                $('#quantity').val(quantityValue)
            };
        });
    
        $('#quantity').on('input', function() {
            const currentValue = parseInt($(this).val());
            if (currentValue > maxValue) $(this).val(maxValue);
        });
    }

    $('#color-wrapper, #size-wrapper').on('change', '.color-radio-input, .size-radio-input', function() {
        if ($(this).attr('name') == 'color-radio-name') {
            const productVariants = grouping_color_test[$(this).val()]?.variants ?? []
            const availableSize = productVariants.map(i => i.size.value)
            $('.size-radio-input').each((_, element) => {
                const variant = productVariants.find(item => item.size.value === +element.value)
                if (availableSize.includes(+element.value) && variant.stock > 0) {
                    element.disabled = false
                } else {
                    element.disabled = true
                }
            })

            productVariants.find(({ size, stock, id }) => {
                if (stock > 0) {
                    $(`.size-radio-input[value="${size.value}"]`).prop('checked', true)
                    return true
                }
                return false
            })
        }

        if ($('.color-radio-input:checked').length && $('.size-radio-input:checked').length) {
            const targetVariant = grouping_color_test[$('.color-radio-input:checked').val()]?.variants.find(i => i.size.value === +$('.size-radio-input:checked').val())
            if (targetVariant) {
                variantId = targetVariant.id
                maxValue = +targetVariant.stock
                quantityValue = 1

                $('#color-readable').text(targetVariant.color)
                $('#size-readable').text(targetVariant.size.label)

                const humanReadablePrice = new Intl.NumberFormat('en-US', {
                    maximumFractionDigits: 2,
                }).format(parseFloat(targetVariant.price));
                $('#product-price').text(`${humanReadablePrice}k`)

                $('#quantity').attr('max', +targetVariant.stock)
                $('#quantity').val(quantityValue)

                $('#quantity, #decrement, #increment, #add-to-cart, #buy-now').prop('disabled', false)

                $('#quantity, #decrement, #increment').off('click')
                handleQuantityInput(maxValue)
            }
        }
    })

    function initialRender() {
        // Check if stock is availlable, set radio input accordingly, else disable the radio 
        
        if (isColorAvailable && isSizeAvailable) {
            sorted_color_test.forEach(([key, { stockNotAvailable, variants }], index) => {
                if (stockNotAvailable) {
                    if (sorted_color_test.length - 1 == index) {
                        variants.forEach(({ size, stock }) => stock === 0 && $(`.size-radio-input[value="${size.value}"]`).prop('disabled', true))
                    }
                    $(`.color-radio-input[value="${key}"]`).prop('disabled', true)
                }
            })
            
            sorted_color_test.find(([key, { variants }]) => {
                if (variants.find(i => i.stock > 0)) {
                    $(`.color-radio-input[value="${key}"]`).prop('checked', true).trigger('change');
                    return true
                }
                return false
            })
        } else {
            !isColorAvailable && $('#color-input-container').addClass('hidden')
            !isSizeAvailable && $('#size-input-container').addClass('hidden')
            if (!isColorAvailable && !isSizeAvailable) {
                // If there are no colors and sizes available, variant is always has one item
                const variant = Object.values(grouping_variant)[0]
                if (+variant.stock > 0) {
                    variantId = variant.id
                    maxValue = +variant.stock
                    const humanReadablePrice = new Intl.NumberFormat('en-US', {
                        maximumFractionDigits: 2,
                    }).format(parseFloat(variant.price));
                    $('#product-price').text(`${humanReadablePrice}k`)
    
                    $('#quantity').attr('max', +variant.stock)
                    quantityValue = quantityValue + 1
                    $('#quantity').val(quantityValue)
    
                    $('#quantity, #decrement, #increment, #add-to-cart, #buy-now').prop('disabled', false)
                    handleQuantityInput(maxValue)
                }
            }
        }
    }

    initialRender()

    $('#add-to-cart').on('click', function(ev) {
        const color = $('.color-radio-input:checked').val()
        const size = $('.size-radio-input:checked').val()
        const cart = new Cart()
        const combineId = [productDetail.id, color, grouping_sizes_test[size]?.value].filter(Boolean).join('.')
        cart.addToCart(combineId, color, grouping_sizes_test[size], quantityValue, variantId)
    })
})

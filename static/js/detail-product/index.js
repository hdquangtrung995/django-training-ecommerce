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
    let variants = JSON.parse($('#variants').text())
    // variants = variants.map(i => ({...i, stock: 0}))
    let maxValue = 1;
    let quantityValue = 0
    
    const grouping_sizes = variants.reduce((acc, curr) => {
        const { size } = curr
        return {...acc, [size.value]: { value: size.value, label: size.label }}
    }, {})
    const processed_product = variants.reduce((acc, curr) => {
        const { color } = curr
        if (acc[color]) {
            const data = [...acc[color].variants, curr]
            return {...acc, [color]: { variants: data.sort(({size: sizeA}, {size: sizeB}) => sizeA.value - sizeB.value), stockNotAvailable: data.every(i => i.stock <= 0) }}
        } else {
            return {...acc, [color]: { variants: [curr], stockNotAvailable: curr.stock <= 0 }}
        }
    }, {})
    const sorted_data = Object.entries(processed_product).sort(([a], [b]) => a.localeCompare(b, 'en', { sensitivity: 'base' }));

    function insertRadioColors() {
        const elements = sorted_data.map(([i, _]) => `
            <div class="relative w-7 h-7 rounded-full border border-black has-[:checked]:border-[#FB8500]">
                <input id="${i}" type="radio" name="color-radio-name" value="${i}" class="color-radio-input appearance-none peer">
                <div class="hidden peer-disabled:block cursor-not-allowed absolute z-20 top-0 left-0 w-full h-full"><div class="ban-icon"></div></div>
                <label for="${i}" class="cursor-pointer absolute w-full h-full top-0 left-0 rounded-full flexRowCenter"><div class="rounded-full w-4 h-4 bg-[${i}]"></div></label>
            </div>
        `) 
        $('#color-wrapper').html(elements.join(''))
    }
    insertRadioColors()
    
    function insertRadioSizes() {
        const elements = Object.values(grouping_sizes).sort((a, b) => a.value - b.value).map(i => `
            <div class="relative w-10 h-10 has-[:checked]:border-[#FB8500]">
                <input id="${i.value}" type="radio" name="size-radio-name" value="${i.value}" class="size-radio-input appearance-none peer">
                <div class="hidden peer-disabled:block cursor-not-allowed absolute z-20 top-0 left-0 w-full h-full"><div class="ban-icon-without-circle"></div></div>
                <label for="${i.value}" class="cursor-pointer absolute top-0 left-0 w-full h-full peer-checked:border-[#FB8500] border rounded-md">
                    <div class="uppercase w-10 h-10 relative flexRowCenter">
                        <span>${i.label}</span>
                        <img class="absolute hidden right-0 bottom-0" src="https://file.hstatic.net/200000525917/file/select-pro_e3e51c75e13340c1805618324bab59f0.png" width="12" height="12" >
                    </div>
                </label>
            </div>
        `)
        $('#size-wrapper').html(elements.join(''))
    }

    insertRadioSizes()

    $('#color-wrapper, #size-wrapper').on('change', '.color-radio-input, .size-radio-input', function() {
        if ($(this).attr('name') == 'color-radio-name') {
            const productVariants = processed_product[$(this).val()]?.variants ?? []

            productVariants.forEach(({ size, stock }) => {
                if (stock <= 0) {
                    $(`.size-radio-input[value="${size.value}"]`).prop('disabled', true)
                } else {
                    $(`.size-radio-input[value="${size.value}"]`).prop('disabled', false)
                }
            })
            productVariants.find(({ size, stock }) => {
                if (stock > 0) {
                    $(`.size-radio-input[value="${size.value}"]`).prop('checked', true)
                    return true
                }
                return false
            })
        }

        if ($('.color-radio-input:checked').length && $('.size-radio-input:checked').length) {
            const targetVariant = processed_product[$('.color-radio-input:checked').val()]?.variants.find(i => i.size.value === +$('.size-radio-input:checked').val())
            if (targetVariant) {
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
                handleQuantityInput(maxValue, quantityValue)
            }
        }
    })

    function initialRender() {
        // Check if stock is availlable, set radio input accordingly, else disable the radio 
        sorted_data.forEach(([key, { stockNotAvailable, variants }], index) => {
            if (stockNotAvailable) {
                if (sorted_data.length - 1 == index) {
                    variants.forEach(({ size, stock }) => stock === 0 && $(`.size-radio-input[value="${size.value}"]`).prop('disabled', true))
                }
                $(`.color-radio-input[value="${key}"]`).prop('disabled', true)
            }
        })

        sorted_data.find(([key, { variants }]) => {
            if (variants.find(i => i.stock > 0)) {
                $(`.color-radio-input[value="${key}"]`).prop('checked', true).trigger('change');
                return true
            }
            return false
        })
    }

    initialRender()
})

function handleQuantityInput(maxValue, quantityValue) {

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

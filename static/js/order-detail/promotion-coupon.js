class PromotionCoupon {
    constructor() {

        this.freeshipRadioName = 'freeship-radio'
        this.freeshipSectionList = 'free-ship-section'

        this.couponSectionList = 'coupon-section'
        this.couponRadioName = 'coupon-radio'
    }

    promotionItemString(promotionItem, radioName, deliveryFee=0) {
        const dialogId = promotionItem.code.concat('-', promotionItem.id)
        return `
            <label class="cursor-pointer flexRow gap-2 has-[:disabled]:cursor-not-allowed">
                <input id="${promotionItem.code}" type="radio" name="${radioName}" class="hidden peer" value="${promotionItem.code}" ${(radioName === this.freeshipRadioName && deliveryFee === 0) || (radioName === this.couponRadioName && !promotionItem.is_valid) ? 'disabled' : ''} />
                
                <div class="w-full flexRow gap-4 p-2 rounded-md border-2 border-gray-300 peer-checked:border-blue-500 peer-disabled:bg-gray-300 peer-disabled:text-gray-400">
                    <div>
                        <img class="m-auto" src="https://file.hstatic.net/1000360022/file/fast-delivery_322f7fa602ff423a9f3adce662e8ad4d.png" width="30" height="30" >
                    </div>
                    <div class="flexCol">
                        <strong class="capitalize">${promotionItem.name}</strong>
                        <p>${promotionItem.description}</p>
                        <span>${convertDecimalToHumanReadable(promotionItem.discount_variant.discount_value, '').concat(promotionItem.discount_variant.discount_type.label)}</span>
                    </div>
                    <button data-dialog="yes" class="self-start ml-auto" onclick="document.querySelector('#${dialogId}').showModal()"><i class="fa fa-info-circle fa-lg text-blue-400"></i></button>
                    <dialog id="${dialogId}" class="w-[500px] p-4 rounded-md">
                        <div class="flexCol w-full h-full gap-4">
                            <p>${promotionItem.description}</p>
                            <div>one</div>
                            <div>two</div>
                            <button data-dialog="yes" class="seeAllButton mt-auto" onclick="document.querySelector('#${dialogId}').close()">close</button>
                        </div>
                    </dialog>
                </div>
            </label>
        `
    }

    renderViewMoreButton(targetContainerId) {
        const buttonId = 'button'.concat('-', targetContainerId)
        const elementString = `<button id="${buttonId}" data-expand="false" class="text-blue-500 hover:text-blue-700 absolute bottom-[-6px] w-full bg-white/[.8] backdrop-blur-xs disabled:cursor-not-allowed disabled:text-gray-300">view more</button>`
        const element = $(elementString)

        element.on('click', function() {
            const isExpand = $(`#${buttonId}`).attr('data-expand')
            if (isExpand === 'true') {
                $(`#${buttonId}`).attr('data-expand', 'false')
                $(`#${buttonId}`).text('view more')
                $(`#${targetContainerId}`).addClass('max-h-24').removeClass('pb-6')
            } else {
                $(`#${buttonId}`).attr('data-expand', 'true')
                $(`#${buttonId}`).text('view less')
                $(`#${targetContainerId}`).removeClass('max-h-24').addClass('pb-6')
            }
        })

        $(`#${targetContainerId}`).append(element)
    }

    renderFreeship(promotions, deliveryFee) {
        const freeshipPromo = promotions.filter(i => i.promotion_type.type === 3)
        $(`#${this.freeshipSectionList}`).addClass('max-h-24')
        let element = ''
        freeshipPromo.forEach(item => {
            element += this.promotionItemString(item, this.freeshipRadioName, deliveryFee)
        })
        $(`#${this.freeshipSectionList}`).html($(element))
        if (freeshipPromo.length > 1) this.renderViewMoreButton(this.freeshipSectionList)
    }

    renderCoupon(promotions) {
        const couponPromo = promotions.filter(i => i.promotion_type.type === 1)
        $(`#${this.couponSectionList}`).addClass('max-h-24')
        let element = ''
        couponPromo.forEach(item => {
            element += this.promotionItemString(item, this.couponRadioName)
        })
        $(`#${this.couponSectionList}`).html($(element))
        if (couponPromo.length > 1) this.renderViewMoreButton(this.couponSectionList)
    }

    setDeliveryPromotionDisableAttrs(value) {
        if (value) {
            $(`#${this.freeshipSectionList}`).find('input, button:not([data-expand], [data-dialog])').prop('disabled', value)
        } else {
            $(`#${this.freeshipSectionList}`).find(':disabled').prop('disabled', value)
        }
        $(`input[name="${this.freeshipRadioName}"]`).prop('checked', false);
    }
}

export default PromotionCoupon;

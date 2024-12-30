class DeliveryFee {
    #csrf_token
    
    constructor(csrf_token, onOptionChange) {
        this.#csrf_token = csrf_token
        this.onOptionChange = onOptionChange
        this.provinceId = 'province-option' // This was set in ecommerce/forms/delivery_fee.py
        this.districtId = 'district-option' // This was set in ecommerce/forms/delivery_fee.py
        this.wardId = 'ward-option' // This was set in ecommerce/forms/delivery_fee.py
        this.submitDeliveryFeeId = 'submit-delivery-fee'
    }

    getDeliveryFee(districtId, wardId, onSuccess, onError, onBeforeSend) {
        $.ajax({
            url: window.location.origin.concat('/delivery/fee/'),
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ districtId, wardId }),
            headers: {
                "X-CSRFToken": this.#csrf_token
            },
            beforeSend: onBeforeSend,
            success: onSuccess,
            error: function(xhr, status, error) {
                onError?.(xhr, status, error)
                console.log('status: ', status);
                console.error('error: ', error);
            }
        });
    }

    fetchDelivery(payload={}, onSuccess, onError, onBeforeSend) {
        let body = {}
        if (payload.provinceId) body.province = payload.provinceId;
        if (payload.districtId) body.district = payload.districtId;
        if (payload.wardId) body.ward = payload.wardId;

        $.ajax({
            url: window.location.origin.concat('/delivery/fee'), // API endpoint stringformat
            method: "GET", // HTTP method
            contentType: "application/json", // Data type to send
            data: body, // Data payload
            headers: {
                "X-CSRFToken": this.#csrf_token
            },
            beforeSend: onBeforeSend,
            success: onSuccess,
            error: function(xhr, status, error) {
                onError?.(status, error)
                console.error('error: ', status, error);
            }
        });
    }

    registerProvinceOption() {
        const self = this
        this.fetchDelivery({}, function(response) {
            let option = ''
            const optionString = (value, label) => `<option value="${value}" ${value == 0 ? 'selected' : ''}>${label}</option>`
            response.data.forEach(({value, label}) => option += optionString(value, label))

            $(`#${self.provinceId}`).prop('disabled', false)
            $(`#${self.provinceId}`).html(option)

            // $(`#${this.provinceId}`).off('change')
            $(`#${self.provinceId}`).on('change', function() {
                self.disableDeliveryOption()
                const value = $(this).val()
                if (value !== 0) {
                    self.fetchDelivery({ provinceId: value }, function success(response) {
                        self.registerDistrictOption(self, response)
                        // self.provinceValue = value
                        
                        $(`#${self.wardId}`).prop('disabled', true)
                        $(`#${self.wardId}`).html(`<option value="0">N/A</option>`)
                        // self.wardValue = null
                        $(`#${self.submitDeliveryFeeId}`).prop('disabled', true)
                    })
                }
            })
        })
    }

    registerDistrictOption(self, provinceResponse) {
        let option = ''
        const optionString = (value, label) => `<option value="${value}" ${value == 0 ? 'selected' : ''}>${label}</option>`
        provinceResponse.data.forEach(({value, label}) => option += optionString(value, label))

        $(`#${this.districtId}`).prop('disabled', false)
        $(`#${this.districtId}`).html(option)

        $(`#${this.districtId}`).off('change')
        $(`#${this.districtId}`).on('change', function() {
            self.disableDeliveryOption()
            const value = $(this).val()
            if (value !== 0) {
                self.fetchDelivery({ districtId: value }, function(response) {
                    self.registerWardOption(self, response)
                    // self.districtValue = value
                })
            }
        })
    }

    registerWardOption(self, wardResponse) {
        let option = ''
        const optionString = (value, label) => `<option value="${value}" ${value == 0 ? 'selected' : ''}>${label}</option>`
        wardResponse.data.forEach(({value, label}) => option += optionString(value, label))

        $(`#${self.wardId}`).prop('disabled', false)
        $(`#${self.wardId}`).html(option)

        $(`#${self.wardId}`).off('change')
        $(`#${self.wardId}`).on('change', function() {
            self.disableDeliveryOption()
            const value = $(this).val()
            if (value !== 0) {
                // self.wardValue = value
                $(`#${self.submitDeliveryFeeId}`).prop('disabled', false)
            }
        })
    }


    registerDeliveryFeeClickEvent(onSuccess) {
        const self = this
        $(`#${this.submitDeliveryFeeId}`).on('click', function(event) {
            event.preventDefault()
            $(this).prop('disabled', true)

            const district = $(`#${self.districtId}`).val()
            const ward = $(`#${self.wardId}`).val()

            self.getDeliveryFee(
                district,
                ward,
                function(response) {
                    $(this).prop('disabled', false)
                    $(`#${self.submitDeliveryFeeId} i`).hide();
                    $(`#${self.submitDeliveryFeeId} span`).show();
                    if (response.data?.total) {
                        onSuccess?.(response.data.total)
                    }
                }.bind(this),
                function(xhr, status, error) {
                    if (xhr.responseJSON && xhr.responseJSON?.type) {
                        const type = xhr.responseJSON.type
                        type === "not_supported" ? true : false                    
                    }
                    $(this).prop('disabled', false)
                    $(`#${self.submitDeliveryFeeId} i`).hide();
                    $(`#${self.submitDeliveryFeeId} span`).show();

                    alert('Cannot calculate delivery fee, Please try again!')
                }.bind(this),
                function() {
                    $(`#${self.submitDeliveryFeeId} i`).show();
                    $(`#${self.submitDeliveryFeeId} span`).hide();
                }.bind(this)
            )
        })
    }

    disableDeliveryOption() {
        this.onOptionChange()
        $(`#${this.submitDeliveryFeeId}`).prop('disabled', true)
    }
}

export default DeliveryFee
